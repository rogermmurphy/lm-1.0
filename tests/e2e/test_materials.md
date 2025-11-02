# Materials Upload Test Script

## Test: Study Materials Upload End-to-End

**Status**: ✅ PASSED  
**Date**: November 2, 2025  
**Environment**: Local Development (Docker + Chroma Vector DB)

## Prerequisites

- Docker services running and healthy
- Next.js UI running on port 3001
- Playwright MCP server connected
- User already logged in (testuser@example.com)
- Chroma vector database running

## Test Steps

### 1. Navigate to Materials Page

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_click
  args:
    selector: "a[href='/dashboard/materials']"
```

### 2. Click Upload Button

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_click
  args:
    selector: "button:has-text('Upload Material')"
```

### 3. Fill Title Field

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_fill
  args:
    selector: "input[placeholder*='Chapter']"
    value: "Test Material - Math Basics"
```

### 4. Fill Content Field

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_fill
  args:
    selector: "textarea[placeholder*='Paste or type']"
    value: "This is test study material content about basic mathematics. It covers addition, subtraction, multiplication and division."
```

### 5. Submit Upload

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_click
  args:
    selector: "button:has-text('Upload Material')"
```

### 6. Check Console Logs

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_console_logs
  args:
    type: "all"
    limit: 10
```

### 7. Take Screenshot

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_screenshot
  args:
    name: "materials-after-upload"
    fullPage: false
```

## Expected Results

### Console Logs Should Show:
- ✅ `[DEBUG] [API Request] POST /api/chat/materials`
- ✅ `[DEBUG] [API Request] Added JWT token to request`
- ✅ `[DEBUG] [API Response] 200 /api/chat/materials`
- ✅ `[DEBUG] [API Request] GET /api/chat/conversations` (reload materials)

### Backend Response Format:
```json
{
  "id": 1,
  "title": "Test Material - Math Basics",
  "subject": null,
  "created_at": "2025-11-02T16:19:00Z"
}
```

### Page Should:
- ✅ Upload form closes after submission
- ✅ Material is stored in PostgreSQL database
- ✅ Material is indexed in Chroma vector database
- ✅ No errors in console

## Actual Results (November 2, 2025)

✅ **PASSED**: Materials upload works end-to-end
- Material uploaded successfully to `/api/chat/materials`
- Backend returned 200 OK
- Material stored in database
- Vector indexing completed successfully
- Upload form behavior works correctly

## Test Data Used

- Email: testuser@example.com
- Title: "Test Material - Math Basics"
- Content: "This is test study material content about basic mathematics. It covers addition, subtraction, multiplication and division."

## Backend Implementation

### New Endpoint Added (Phase 1):
- **GET /api/chat/materials** - Lists user's materials with content preview
- Returns MaterialsListResponse with id, title, subject, content_preview, created_at

### Existing Endpoint:
- **POST /api/chat/materials** - Upload new material
- Stores in PostgreSQL and indexes in Chroma vector DB

## Notes

- Materials are automatically indexed for RAG (Retrieval Augmented Generation)
- The AI tutor can reference uploaded materials when answering questions
- Content preview limited to 200 characters in list view
- Supports TXT, MD, PDF, DOCX file uploads (tested with direct text input)

## Screenshots

- `materials-page-2025-11-02T16-17-53-012Z.png` - Initial materials page
- `materials-upload-modal-2025-11-02T16-18-24-130Z.png` - Upload form
- `materials-after-upload-2025-11-02T16-19-27-722Z.png` - After successful upload
