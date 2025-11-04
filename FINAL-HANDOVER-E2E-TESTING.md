# FINAL HANDOVER: E2E Testing & Remediation Task
**Mode**: ZERO TOLERANCE + YOLO MODE  
**Scope**: Complete E2E testing with systematic error remediation
**Current Status**: System partially working, 3 critical errors remain

---

## ⚠️ MANDATORY READING (IN ORDER)

**You MUST read and understand these documents before making ANY changes:**

### 1. System Architecture (30 min)
- `docs/alpha-0.9/SYSTEM-ARCHITECTURE.md` - Service architecture
- `docs/alpha-0.9/INTEGRATION-ARCHITECTURE.md` - How services communicate
- `docker-compose.yml` - All services, ports, dependencies

### 2. Current Status (15 min)
- `E2E-TEST-FINAL-STATUS.md` - What was accomplished (CORS fixed)
- `ACTUAL-STATUS.md` - What the previous developer broke
- This document - Current errors and research requirements

### 3. CORS Fix Understanding (10 min)
- `services/api-gateway/nginx.conf` - Lines 65-75 (proxy_hide_header directives)
- Understand WHY this fixes duplicate CORS headers
- Test: `curl -I http://localhost/api/groups/` should show ONE Access-Control-Allow-Origin header

### 4. Testing Methodology (10 min)
- `.clinerules/zero-tolerance-testing.md` - No errors tolerated
- `.clinerules/functional-testing-requirement.md` - Test user workflows
- Playwright MCP testing workflow

---

## 🎯 CURRENT ERRORS (From Browser Console)

```javascript
// ERROR 1 & 2: Classes and Assignments - 401 Unauthorized
GET http://localhost/api/classes 401 (Unauthorized)
GET http://localhost/api/assignments 401 (Unauthorized)

// ERROR 3: Groups - 404 Not Found  
GET http://localhost/api/groups/my-groups/ 404 (Not Found)
// Note: I just fixed this (removed trailing slash), needs web-app restart

// ERROR 4: Groups - TypeError
TypeError: n.map is not a function
// Backend returning wrong data type (not an array)
```

---

## 🔬 RESEARCH REQUIREMENTS (Use Sequential Thinking Tool)

### For Each Error, You Must:

1. **Understand the Request Flow**
   ```
   Browser → http://localhost:3000 (Next.js)
     ↓ Fetch API
   Gateway → http://localhost/api/* (Nginx)
     ↓ proxy_pass
   Service → http://[container]:port/api/* (FastAPI)
     ↓ SQL Query
   Database → lm-postgres:5432/littlemonster
   ```

2. **Use Sequential Thinking**
   - Launch sequential thinking tool
   - Break down the problem step by step
   - Consider: What should happen? What is happening? Why the difference?
   - Generate hypothesis
   - Verify hypothesis
   - Implement fix

3. **Research Each Layer**
   - Frontend: What data does the UI expect?
   - Network: What is actually being sent?
   - Backend: What does the endpoint return?
   - Database: Does the data exist?

---

## 🐛 ERROR ANALYSIS & RESEARCH TASKS

### ERROR 1&2: Classes/Assignments 401 Unauthorized

**Research Questions**:
1. Does the frontend send Authorization header?
2. Check `views/web-app/src/lib/api.ts` - How are auth tokens added?
3. Check `views/web-app/src/contexts/AuthContext.tsx` - Is token stored after login?
4. Test manually: `curl -H "Authorization: Bearer [token]" http://localhost/api/classes`

**Files to Research**:
- `views/web-app/src/lib/api.ts` (API client setup)
- `views/web-app/src/contexts/AuthContext.tsx` (Token storage)
- `services/class-management/src/routes/classes.py` (Auth requirements)

**Sequential Thinking Steps**:
1. Login succeeds → token received
2. Navigate to Classes → fetch /api/classes
3. Question: Is Authorization header included?
4. Hypothesis: Token not being retrieved from storage
5. Verify: Check localStorage in browser DevTools
6. Fix: Ensure API client includes auth header

### ERROR 3: Groups 404 on my-groups

**Status**: FIXED (removed trailing slash from frontend)
**Verification Needed**: Test after web-app restarts

### ERROR 4: Groups TypeError - n.map is not a function

**Research Questions**:
1. What does `/api/groups/` return? (Should be array)
2. Check: `curl http://localhost/api/groups/` - Inspect response
3. Is it returning `{data: [...]}` instead of `[...]`?
4. Does frontend expect array but backend returns object?

**Files to Research**:
- `services/social-collaboration/src/routes/groups.py` - Line 74 `get_groups()` function
- Check what `[dict(row) for row in cur.fetchall()]` returns
- Test: `docker exec lm-social-collab python -c "import psycopg2; ..."`

**Sequential Thinking Steps**:
1. Frontend calls `/api/groups/`
2. Expects: `[{id: 1, name: "..."}, ...]`
3. Backend returns: What actually?
4. Test direct: `curl http://localhost/api/groups/`
5. If returns array → check frontend parsing
6. If returns object → fix backend to return array

---

## 🧪 TESTING PROTOCOL (ZERO TOLERANCE)

### After EVERY Fix:
```bash
# 1. Rebuild if code changed
docker stop [container] && docker rm [container] && docker-compose up -d

# 2. Test with Playwright MCP
playwright_navigate("http://localhost:3000/login")
playwright_fill + playwright_click  # Login
playwright_navigate("http://localhost:3000/dashboard/[page]")
playwright_console_logs(type="error")

# 3. If ANY errors:
#    - Use sequential thinking to analyze
#    - Fix the root cause
#    - Rebuild
#    - Retest SAME page
#    - Repeat until ZERO errors

# 4. Only move to next page when current page is clean
```

---

## 📊 WHAT'S CURRENTLY WORKING

**Backend APIs (Verified with curl)**:
- `/api/groups/` → 200 OK ✅
- `/api/groups/my-groups` → 200 OK ✅
- `/api/notifications/` → 200 OK ✅
- `/api/messages/conversations` → 200 OK ✅

**Frontend Pages (Based on previous testing)**:
- Login ✅
- Dashboard ✅
- Chat ✅
- Flashcards ✅
- Transcribe ✅
- TTS ✅
- Materials ✅

---

## 🎯 YOUR MISSION

### Success Criteria:
- [ ] All 12 pages load without JavaScript errors
- [ ] Classes page shows data (no 401)
- [ ] Assignments page shows data (no 401)
- [ ] Groups page shows groups list (no TypeError)
- [ ] Notifications page works
- [ ] Messages page works
- [ ] Playwright console shows ZERO errors on every page

### Deliverables:
1. Fixed code (with comments explaining what you fixed and why)
2. Test results for all 12 pages
3. Documentation of root causes
4. Prevention strategies for similar issues

---

## 🚀 START HERE

### Step 1: Verify System State
```bash
docker ps  # All containers running?
curl http://localhost:3000  # Frontend loads?
curl http://localhost/api/groups/  # Backend works?
```

### Step 2: Use Sequential Thinking for Each Error
Example for Classes 401:
```
Thought 1: Login returns 200, so auth works
Thought 2: Token should be stored after login
Thought 3: Classes request gets 401, so token not sent
Thought 4: Check if API client adds Authorization header
Thought 5: Hypothesis - token stored but not retrieved
Thought 6: Verify by checking AuthContext implementation
...
```

### Step 3: Fix Systematically
- One error at a time
- Test after each fix
- Document what you learned

---

## 💡 KEY INSIGHTS FROM PREVIOUS WORK

1. **CORS is NOT the problem** - It's been fixed correctly
2. **Backend APIs work** - They return 200 when tested with curl
3. **Frontend integration is broken** - Auth tokens, data parsing
4. **Previous developer's mistake** - Stopped containers unnecessarily
5. **Current state** - Backend fixed, frontend needs integration fixes

---

## 🔥 ZERO TOLERANCE REMINDER

**No excuses. No partial fixes. No "good enough".**

- Test after every change
- Fix errors immediately
- Don't move forward with errors present
- Use sequential thinking for complex issues
- Read the code, understand it, then fix it

You have all the tools, documentation, and context. Now execute flawlessly.
