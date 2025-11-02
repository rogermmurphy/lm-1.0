# Login Test Script

## Test: User Login End-to-End

**Status**: ✅ PASSED  
**Date**: November 2, 2025  
**Environment**: Local Development (Bedrock + Docker)

## Prerequisites

- Docker services running (`docker-compose ps` shows all healthy)
- Next.js UI running on port 3001
- Playwright MCP server connected
- User already registered (use test_registration.md first)

## Test Steps

### 1. Navigate to Login Page

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_navigate
  args:
    url: http://localhost:3001/login
    browserType: chromium
    headless: false
    width: 1280
    height: 720
```

### 2. Fill Email Field

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_fill
  args:
    selector: "input[type='email']"
    value: "testuser@example.com"
```

### 3. Fill Password Field

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_fill
  args:
    selector: "input[type='password']"
    value: "TestPass123!"
```

### 4. Submit Login

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_click
  args:
    selector: "button[type='submit']"
```

### 5. Check Console Logs

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_console_logs
  args:
    type: "all"
    limit: 10
```

### 6. Take Screenshot

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_screenshot
  args:
    name: "after-login-dashboard"
    fullPage: false
```

### 7. Close Browser

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_close
  args: {}
```

## Expected Results

### Console Logs Should Show:
- ✅ `[DEBUG] [API Request] POST /api/auth/login`
- ✅ `[DEBUG] [API Response] 200 /api/auth/login`

### Backend Response Format:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "username": "testuser123",
    "full_name": null,
    "is_verified": false,
    "is_active": true,
    "created_at": "2025-11-02T15:15:00Z"
  }
}
```

### Page Should:
- ✅ Redirect to dashboard after successful login
- ✅ Store tokens in localStorage
- ✅ Display user information in dashboard

## Actual Results (November 2, 2025)

✅ **PASSED**: Login workflow works end-to-end
- Login endpoint returned 200 OK
- Response included both tokens AND user data (AuthResponse)
- User was successfully redirected to dashboard
- No errors in console logs

## Test Data Used

- Email: testuser@example.com
- Password: TestPass123!

## Notes

- Login endpoint was fixed to return AuthResponse (tokens + user data)
- Previously only returned tokens without user data
- Now matches UI expectations
