"""
Study Groups Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..models import (
    StudyGroupCreate, StudyGroupUpdate, StudyGroup,
    GroupMemberAdd, GroupMemberUpdate, GroupMember,
    GroupMessageCreate, GroupMessage
)

router = APIRouter(prefix="/groups", tags=["groups"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


# ============================================================================
# STUDY GROUPS
# ============================================================================

@router.post("/", response_model=dict)
async def create_group(
    group: StudyGroupCreate,
    authorization: Optional[str] = Header(None)
):
    """Create a new study group"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Create group
            cur.execute("""
                INSERT INTO study_groups (name, description, class_id, created_by_user_id, max_members)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, description, class_id, created_by_user_id, is_active, max_members, created_at, updated_at
            """, (group.name, group.description, group.class_id, user_id, group.max_members))
            
            result = cur.fetchone()
            group_id = result['id']
            
            # Add creator as admin
            cur.execute("""
                INSERT INTO study_group_members (group_id, user_id, role)
                VALUES (%s, %s, 'admin')
            """, (group_id, user_id))
            
            conn.commit()
            return {"message": "Study group created", "group": dict(result)}
    finally:
        conn.close()


@router.get("/", response_model=List[dict])
async def get_groups(
    class_id: Optional[int] = None,
    authorization: Optional[str] = Header(None)
):
    """Get all study groups or filter by class"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if class_id:
                cur.execute("""
                    SELECT * FROM study_groups
                    WHERE class_id = %s AND is_active = true
                    ORDER BY created_at DESC
                """, (class_id,))
            else:
                cur.execute("""
                    SELECT * FROM study_groups
                    WHERE is_active = true
                    ORDER BY created_at DESC
                """)
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.get("/my-groups", response_model=List[dict])
async def get_my_groups(
    authorization: Optional[str] = Header(None)
):
    """Get groups I'm a member of"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT g.*, m.role, m.joined_at
                FROM study_groups g
                JOIN study_group_members m ON g.id = m.group_id
                WHERE m.user_id = %s AND g.is_active = true
                ORDER BY m.joined_at DESC
            """, (user_id,))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.get("/{group_id}", response_model=dict)
async def get_group(
    group_id: int,
    authorization: Optional[str] = Header(None)
):
    """Get a specific study group"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM study_groups WHERE id = %s", (group_id,))
            result = cur.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Group not found")
            
            return dict(result)
    finally:
        conn.close()


@router.put("/{group_id}", response_model=dict)
async def update_group(
    group_id: int,
    update: StudyGroupUpdate,
    authorization: Optional[str] = Header(None)
):
    """Update a study group"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check if user is admin
            cur.execute("""
                SELECT role FROM study_group_members
                WHERE group_id = %s AND user_id = %s
            """, (group_id, user_id))
            
            member = cur.fetchone()
            if not member or member['role'] != 'admin':
                raise HTTPException(status_code=403, detail="Only admins can update groups")
            
            # Build update query
            updates = []
            params = []
            if update.name is not None:
                updates.append("name = %s")
                params.append(update.name)
            if update.description is not None:
                updates.append("description = %s")
                params.append(update.description)
            if update.is_active is not None:
                updates.append("is_active = %s")
                params.append(update.is_active)
            if update.max_members is not None:
                updates.append("max_members = %s")
                params.append(update.max_members)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No updates provided")
            
            params.append(group_id)
            cur.execute(f"""
                UPDATE study_groups
                SET {', '.join(updates)}, updated_at = NOW()
                WHERE id = %s
                RETURNING id, name, description, class_id, created_by_user_id, is_active, max_members, created_at, updated_at
            """, params)
            
            result = cur.fetchone()
            conn.commit()
            return {"message": "Group updated", "group": dict(result)}
    finally:
        conn.close()


# ============================================================================
# GROUP MEMBERS
# ============================================================================

@router.post("/{group_id}/members", response_model=dict)
async def add_member(
    group_id: int,
    member: GroupMemberAdd,
    authorization: Optional[str] = Header(None)
):
    """Add a member to a study group"""
    user_id = 1  # Placeholder (admin adding member)
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check if user is admin
            cur.execute("""
                SELECT role FROM study_group_members
                WHERE group_id = %s AND user_id = %s
            """, (group_id, user_id))
            
            admin = cur.fetchone()
            if not admin or admin['role'] not in ['admin', 'moderator']:
                raise HTTPException(status_code=403, detail="Only admins/moderators can add members")
            
            # Add member
            cur.execute("""
                INSERT INTO study_group_members (group_id, user_id, role)
                VALUES (%s, %s, %s)
                RETURNING id, group_id, user_id, role, joined_at
            """, (group_id, member.user_id, member.role))
            
            result = cur.fetchone()
            conn.commit()
            return {"message": "Member added", "member": dict(result)}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="User is already a member")
    finally:
        conn.close()


@router.get("/{group_id}/members", response_model=List[dict])
async def get_members(
    group_id: int,
    authorization: Optional[str] = Header(None)
):
    """Get all members of a study group"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM study_group_members
                WHERE group_id = %s
                ORDER BY joined_at ASC
            """, (group_id,))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.delete("/{group_id}/members/{member_id}")
async def remove_member(
    group_id: int,
    member_id: int,
    authorization: Optional[str] = Header(None)
):
    """Remove a member from a study group"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor() as cur:
            # Check if user is admin
            cur.execute("""
                SELECT role FROM study_group_members
                WHERE group_id = %s AND user_id = %s
            """, (group_id, user_id))
            
            admin = cur.fetchone()
            if not admin or admin['role'] != 'admin':
                raise HTTPException(status_code=403, detail="Only admins can remove members")
            
            cur.execute("""
                DELETE FROM study_group_members
                WHERE id = %s AND group_id = %s
            """, (member_id, group_id))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Member not found")
            
            conn.commit()
            return {"message": "Member removed"}
    finally:
        conn.close()


# ============================================================================
# GROUP MESSAGES
# ============================================================================

@router.post("/{group_id}/messages", response_model=dict)
async def post_message(
    group_id: int,
    message: GroupMessageCreate,
    authorization: Optional[str] = Header(None)
):
    """Post a message to a study group"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check if user is a member
            cur.execute("""
                SELECT id FROM study_group_members
                WHERE group_id = %s AND user_id = %s
            """, (group_id, user_id))
            
            if not cur.fetchone():
                raise HTTPException(status_code=403, detail="Only members can post messages")
            
            cur.execute("""
                INSERT INTO study_group_messages (group_id, user_id, message_text)
                VALUES (%s, %s, %s)
                RETURNING id, group_id, user_id, message_text, is_deleted, created_at
            """, (group_id, user_id, message.message_text))
            
            result = cur.fetchone()
            conn.commit()
            return {"message": "Message posted", "group_message": dict(result)}
    finally:
        conn.close()


@router.get("/{group_id}/messages", response_model=List[dict])
async def get_messages(
    group_id: int,
    limit: int = 50,
    authorization: Optional[str] = Header(None)
):
    """Get messages from a study group"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM study_group_messages
                WHERE group_id = %s AND is_deleted = false
                ORDER BY created_at DESC
                LIMIT %s
            """, (group_id, limit))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
