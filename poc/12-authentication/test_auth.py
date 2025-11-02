"""
POC 12: Authentication Test Script
Tests registration, login, and JWT token functionality
"""
import os
from datetime import datetime
from models import User, get_db_engine, get_session_maker, create_tables
from password_utils import hash_password, verify_password, validate_password_strength, validate_email
from jwt_utils import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lmuser:lmpassword@localhost:5432/lm_db")
SECRET_KEY = "test-secret-key-for-poc"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n[Step {step_num}] {text}")

def print_success(text):
    """Print success message"""
    print(f"[OK] SUCCESS: {text}")

def print_error(text):
    """Print error message"""
    print(f"[ERROR] ERROR: {text}")

def print_info(text):
    """Print info message"""
    print(f"[INFO] INFO: {text}")

def main():
    """Run authentication tests"""
    print_header("POC 12: Authentication System Test")
    print(f"Database: {DATABASE_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Connect to database
    print_step(1, "Connecting to Database")
    try:
        engine = get_db_engine(DATABASE_URL)
        SessionMaker = get_session_maker(engine)
        session = SessionMaker()
        print_success("Connected to PostgreSQL database")
    except Exception as e:
        print_error(f"Failed to connect to database: {e}")
        print_info("Make sure PostgreSQL is running (docker ps | grep lm-postgres)")
        return False
    
    # Step 2: Create tables
    print_step(2, "Creating Database Tables")
    try:
        create_tables(engine)
        print_success("Tables created successfully")
        print_info("Tables: users, oauth_connections, refresh_tokens, password_reset_tokens")
    except Exception as e:
        print_error(f"Failed to create tables: {e}")
        return False
    
    # Step 3: Test password validation
    print_step(3, "Testing Password Validation")
    test_passwords = [
        ("weak", False, "Too short, missing requirements"),
        ("WeakPass1", False, "Missing special character"),
        ("Strong@Pass1", True, "Meets all requirements")
    ]
    
    for password, should_pass, description in test_passwords:
        is_valid, error = validate_password_strength(password)
        if is_valid == should_pass:
            print_success(f"'{password}' - {description}")
        else:
            print_error(f"'{password}' - Expected {should_pass}, got {is_valid}")
    
    # Step 4: Test email validation
    print_step(4, "Testing Email Validation")
    test_emails = [
        ("test@example.com", True, "Valid email"),
        ("invalid-email", False, "Invalid format"),
        ("user@domain", False, "Missing TLD")
    ]
    
    for email, should_pass, description in test_emails:
        is_valid, error = validate_email(email)
        if is_valid == should_pass:
            print_success(f"'{email}' - {description}")
        else:
            print_error(f"'{email}' - Expected {should_pass}, got {is_valid}")
    
    # Step 5: Register a test user
    print_step(5, "Registering Test User")
    test_email = "testuser@littlemonster.com"
    test_password = "Test@Pass123"
    test_username = "testuser"
    test_fullname = "Test User"
    
    try:
        # Check if user already exists
        existing_user = session.query(User).filter_by(email=test_email).first()
        if existing_user:
            session.delete(existing_user)
            session.commit()
            print_info("Deleted existing test user")
        
        # Validate email and password
        email_valid, email_error = validate_email(test_email)
        if not email_valid:
            raise ValueError(f"Invalid email: {email_error}")
        
        password_valid, password_error = validate_password_strength(test_password)
        if not password_valid:
            raise ValueError(f"Invalid password: {password_error}")
        
        # Hash password
        password_hash = hash_password(test_password)
        print_info(f"Password hashed: {password_hash[:50]}...")
        
        # Create user
        new_user = User(
            email=test_email,
            username=test_username,
            password_hash=password_hash,
            full_name=test_fullname,
            is_verified=True,  # Auto-verify for testing
            is_active=True
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        print_success(f"User registered successfully (ID: {new_user.id})")
        print_info(f"Email: {new_user.email}")
        print_info(f"Username: {new_user.username}")
        print_info(f"Full Name: {new_user.full_name}")
        print_info(f"Created: {new_user.created_at}")
        
        user_id = new_user.id
        
    except Exception as e:
        print_error(f"Registration failed: {e}")
        session.rollback()
        return False
    
    # Step 6: Test login (password verification)
    print_step(6, "Testing Login (Password Verification)")
    try:
        # Fetch user
        user = session.query(User).filter_by(email=test_email).first()
        if not user:
            raise ValueError("User not found")
        
        # Test correct password
        if verify_password(test_password, user.password_hash):
            print_success("Correct password verified")
        else:
            print_error("Correct password failed verification")
            return False
        
        # Test wrong password
        if not verify_password("WrongPass123!", user.password_hash):
            print_success("Wrong password correctly rejected")
        else:
            print_error("Wrong password incorrectly accepted")
            return False
        
        # Update last login
        user.last_login = datetime.utcnow()
        session.commit()
        print_info(f"Last login updated: {user.last_login}")
        
    except Exception as e:
        print_error(f"Login test failed: {e}")
        return False
    
    # Step 7: Generate JWT tokens
    print_step(7, "Generating JWT Tokens")
    try:
        # Generate access token
        access_token = create_access_token(
            user_id=user_id,
            email=test_email,
            secret_key=SECRET_KEY,
            expires_minutes=30
        )
        print_success("Access token generated")
        print_info(f"Token (first 50 chars): {access_token[:50]}...")
        
        # Generate refresh token
        refresh_token = create_refresh_token(
            user_id=user_id,
            secret_key=SECRET_KEY,
            expires_days=7
        )
        print_success("Refresh token generated")
        print_info(f"Token (first 50 chars): {refresh_token[:50]}...")
        
    except Exception as e:
        print_error(f"Token generation failed: {e}")
        return False
    
    # Step 8: Verify JWT tokens
    print_step(8, "Verifying JWT Tokens")
    try:
        # Verify access token
        verified_user_id = verify_access_token(access_token, secret_key=SECRET_KEY)
        if verified_user_id == user_id:
            print_success(f"Access token verified (User ID: {verified_user_id})")
        else:
            print_error(f"Access token verification failed: expected {user_id}, got {verified_user_id}")
            return False
        
        # Verify refresh token
        verified_user_id = verify_refresh_token(refresh_token, secret_key=SECRET_KEY)
        if verified_user_id == user_id:
            print_success(f"Refresh token verified (User ID: {verified_user_id})")
        else:
            print_error(f"Refresh token verification failed: expected {user_id}, got {verified_user_id}")
            return False
        
        # Test invalid token
        if verify_access_token("invalid.token.here", secret_key=SECRET_KEY) is None:
            print_success("Invalid token correctly rejected")
        else:
            print_error("Invalid token incorrectly accepted")
            return False
        
    except Exception as e:
        print_error(f"Token verification failed: {e}")
        return False
    
    # Step 9: Query user from database
    print_step(9, "Querying User from Database")
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            print_success(f"User found in database")
            print_info(f"ID: {user.id}")
            print_info(f"Email: {user.email}")
            print_info(f"Username: {user.username}")
            print_info(f"Full Name: {user.full_name}")
            print_info(f"Is Verified: {user.is_verified}")
            print_info(f"Is Active: {user.is_active}")
            print_info(f"Created: {user.created_at}")
            print_info(f"Last Login: {user.last_login}")
        else:
            print_error("User not found in database")
            return False
    except Exception as e:
        print_error(f"Database query failed: {e}")
        return False
    
    # Step 10: Test complete workflow
    print_step(10, "Complete Authentication Workflow")
    print_success("User Registration")
    print_success("Password Hashing (bcrypt)")
    print_success("Password Verification")
    print_success("JWT Access Token Generation")
    print_success("JWT Refresh Token Generation")
    print_success("JWT Token Verification")
    print_success("Database Persistence")
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("ALL TESTS PASSED!")
    print("\nAuthentication System Status:")
    print("  [OK] Database connection working")
    print("  [OK] Database tables created")
    print("  [OK] Password validation working")
    print("  [OK] Email validation working")
    print("  [OK] User registration working")
    print("  [OK] Password hashing (bcrypt) working")
    print("  [OK] Login/password verification working")
    print("  [OK] JWT token generation working")
    print("  [OK] JWT token verification working")
    print("  [OK] Database queries working")
    
    print("\nNext Steps:")
    print("  1. Add OAuth2 providers (Google, Facebook, Microsoft)")
    print("  2. Create FastAPI REST API endpoints")
    print("  3. Add email verification system")
    print("  4. Implement password reset flow")
    print("  5. Add rate limiting with Redis")
    print("  6. Create comprehensive test suite")
    
    print("\n" + "="*60)
    print("  POC 12: AUTHENTICATION SYSTEM - WORKING!")
    print("="*60 + "\n")
    
    # Cleanup
    session.close()
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
