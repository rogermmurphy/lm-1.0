# Comprehensive E2E Test Guide

## Test Script Template

The E2E test script at `tests/e2e/test_chat_history.py` serves as a template for comprehensive application testing. It demonstrates:

1. **Login Flow** - Using `localStorage.setItem('hasSeenOnboarding', 'true')` to bypass modal
2. **Navigation** - Going to specific pages
3. **Interactions** - Clicking elements
4. **Console Logging** - Capturing all console output for debugging
5. **DOM Inspection** - Checking if elements render
6. **Screenshots** - Taking before/after images
7. **Verification** - Asserting expected results

## Expanding the Test Script

### Current Test Coverage
```
✅ Login functionality
✅ Chat page load
✅ Onboarding modal bypass
✅ Conversation list loading
✅ Conversation click
❌ Message history display (blocked by missing code deployment)
```

### Buttons/Features to Add

**Dashboard Pages:**
- Classes page - Create class, view classes, click class details
- Assignments page - Create assignment, view assignments
- Flashcards page - Create flashcard deck, study mode
- Chat page - Send message, load history (Phase 2)
- Transcribe page - Upload audio file
- TTS page - Generate speech from text
- Materials page - Upload study material
- Notifications page - View notifications, mark as read
- Messages page - Send message to user
- Groups page - Create group, join group

**For Each Feature:**
1. Navigate to page
2. Set localStorage if needed (onboarding, etc.)
3. Take screenshot
4. Click primary button
5. Fill form fields
6. Submit
7. Take screenshot
8. Verify success (check DOM for new element)
9. Check console logs for errors
10. Assert results

## Complete Test Structure

```python
async def test_full_application():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Listen to all console
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        # 1. Login
        await test_login(page)
        
        # 2. Dashboard
        await test_dashboard(page)
        
        # 3. Classes
        await test_classes(page)
        
        # 4. Assignments  
        await test_assignments(page)
        
        # 5. Chat
        await test_chat(page)
        
        # 6. Flashcards
        await test_flashcards(page)
        
        # 7. Transcribe
        await test_transcribe(page)
        
        # 8. TTS
        await test_tts(page)
        
        # 9. Materials
        await test_materials(page)
        
        # 10. Notifications
        await test_notifications(page)
        
        # 11. Messages
        await test_messages(page)
        
        # 12. Groups
        await test_groups(page)
        
        # Verify no errors
        errors = [msg for msg in console_messages if 'error' in msg.lower() and 'favicon' not in msg.lower()]
        assert len(errors) == 0, f"Found {len(errors)} errors"
        
        await browser.close()
```

## Test Delivery Parameters

### Requirements for Each Test
1. **Login First** - Always start by logging in (test@test.com / Test1234!)
2. **Modal Bypass** - `localStorage.setItem('hasSeenOnboarding', 'true')`
3. **Unique Selectors** - Use specific CSS selectors or test IDs
4. **Wait for Network** - `await page.wait_for_load_state("networkidle")`
5. **Screenshot Evidence** - Before and after each action
6. **Console Capture** - Save all console output
7. **Error Checking** - Verify no errors except acceptable ones
8. **Cleanup** - Close browser at end

### Success Criteria
- ✅ Feature completes user workflow
- ✅ Expected result appears in DOM
- ✅ Console shows expected API calls
- ✅ No errors (except favicon 404)
- ✅ Screenshots show correct state

### Failure Handling
- ❌ Take screenshot on error
- ❌ Save console logs
- ❌ Print traceback
- ❌ Return False (test fails)

## How to Add New Test

**Example: Testing "Create Class" button**

```python
async def test_create_class(page):
    """Test creating a new class"""
    print("\n[TEST] Create Class")
    
    # Navigate
    await page.goto("http://localhost:3000/dashboard/classes")
    await page.wait_for_load_state("networkidle")
    
    # Bypass modal
    await page.evaluate("localStorage.setItem('hasSeenOnboarding', 'true')")
    await page.reload()
    
    # Screenshot before
    await page.screenshot(path="class-before.png")
    
    # Click "Create Class" button
    await page.click("button:has-text('Create Class')")
    await asyncio.sleep(0.5)
    
    # Fill form
    await page.fill("#className", "Test Class")
    await page.fill("#subject", "Math")
    await page.click("button[type='submit']")
    await asyncio.sleep(1)
    
    # Screenshot after
    await page.screenshot(path="class-after.png")
    
    # Verify
    classes = await page.query_selector_all(".class-card")
    assert len(classes) > 0, "No classes found"
    
    print(f"✅ Created class, found {len(classes)} total")
    return True
```

## Next Steps

1. **Fix AuthProvider SSR** - Add proper client-side rendering
2. **Expand test_chat_history.py** - Add more page tests
3. **Run full suite** - Test all 12 dashboard pages
4. **Fix issues found** - Iterate until zero errors
5. **Document results** - Update handover with findings

## Files

**Test Script:** `tests/e2e/test_chat_history.py` (base template)
**Results:** `tests/e2e/CHAT-HISTORY-TEST-FINAL.md`
**Handover:** This file

## Commands

```bash
# Run current test
python tests/e2e/test_chat_history.py

# Run expanded test (once created)
python tests/e2e/test_full_app.py

# Check logs
docker logs lm-web-app --tail 50
```

## Notes

- Playwright opens browser visibly (headless=False) for debugging
- Screenshots saved to working directory
- Test credentials: test@test.com / Test1234!
- Modal bypass required on every page
- Wait 1-2 seconds after actions for async operations
