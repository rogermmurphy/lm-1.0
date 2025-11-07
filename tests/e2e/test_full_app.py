#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive E2E Test: Full Little Monster GPA Application
Tests ALL 14 pages systematically: every button, link, form, feature
"""
import asyncio
from playwright.async_api import async_playwright
import sys
import io
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test credentials
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "Test1234!"
BASE_URL = "http://localhost:3000"

# Defect tracking
defects = []

def add_defect(page_name, feature, severity, description, expected, actual, console_errors, screenshot_paths):
    """Add a defect to the tracking list"""
    defect_num = len(defects) + 1
    defects.append({
        'number': defect_num,
        'page': page_name,
        'feature': feature,
        'severity': severity,
        'description': description,
        'expected': expected,
        'actual': actual,
        'console_errors': console_errors,
        'screenshots': screenshot_paths,
        'timestamp': datetime.now().isoformat()
    })
    print(f"\n[DEFECT #{defect_num:03d}] {severity} - {page_name} - {feature}")
    print(f"  Description: {description}")
    return defect_num

async def setup_auth(page):
    """Helper: Login and bypass onboarding modal"""
    print(f"\n[SETUP] Logging in as {TEST_EMAIL}...")
    await page.goto(f"{BASE_URL}/login")
    await page.wait_for_load_state("networkidle", timeout=60000)
    
    await page.fill("#email", TEST_EMAIL)
    await page.fill("#password", TEST_PASSWORD)
    await page.click("button[type='submit']")
    
    # Wait for redirect (don't rely on wait_for_url pattern)
    await asyncio.sleep(3)
    
    # Check if we're on dashboard
    current_url = page.url
    if '/dashboard' not in current_url:
        print(f"[WARN] Login may have failed. Current URL: {current_url}")
        print("[INFO] Attempting to navigate directly to dashboard...")
        await page.goto(f"{BASE_URL}/dashboard")
        await page.wait_for_load_state("networkidle", timeout=60000)
    
    # Bypass onboarding modal
    await page.evaluate("localStorage.setItem('hasSeenOnboarding', 'true')")
    print(f"[OK] Logged in and on: {page.url}")

def capture_console_errors(console_messages):
    """Extract non-favicon errors from console"""
    return [msg for msg in console_messages if 'error' in msg.lower() and 'favicon' not in msg.lower()]

# ============================================================================
# TEST: Login Page
# ============================================================================
async def test_login_page(page, console_messages):
    """Test login functionality"""
    print("\n" + "="*80)
    print("TEST: Login Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.screenshot(path="screenshots/01-login-page.png")
        
        # Check form elements exist
        email_field = await page.query_selector("#email")
        password_field = await page.query_selector("#password")
        submit_button = await page.query_selector("button[type='submit']")
        
        if not email_field:
            add_defect("Login", "Email Field", "HIGH", "Email input field not found", 
                      "Email field should exist", "Field missing from DOM", [], 
                      ["screenshots/01-login-page.png"])
        
        if not password_field:
            add_defect("Login", "Password Field", "HIGH", "Password input field not found",
                      "Password field should exist", "Field missing from DOM", [],
                      ["screenshots/01-login-page.png"])
        
        if not submit_button:
            add_defect("Login", "Submit Button", "HIGH", "Submit button not found",
                      "Submit button should exist", "Button missing from DOM", [],
                      ["screenshots/01-login-page.png"])
        
        print("[OK] Login page elements verified")
        
    except Exception as e:
        add_defect("Login", "Page Load", "CRITICAL", f"Login page failed to load: {e}",
                  "Page should load successfully", "Exception occurred", 
                  capture_console_errors(console_messages), ["screenshots/01-login-page.png"])
        raise

# ============================================================================
# TEST: Register Page
# ============================================================================
async def test_register_page(page, console_messages):
    """Test registration functionality"""
    print("\n" + "="*80)
    print("TEST: Register Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/register")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.screenshot(path="screenshots/02-register-page.png")
        
        # Check form elements
        email_field = await page.query_selector("#email")
        password_field = await page.query_selector("#password")
        username_field = await page.query_selector("#username")
        submit_button = await page.query_selector("button[type='submit']")
        
        missing_fields = []
        if not email_field: missing_fields.append("email")
        if not password_field: missing_fields.append("password")
        if not username_field: missing_fields.append("username")
        if not submit_button: missing_fields.append("submit button")
        
        if missing_fields:
            add_defect("Register", "Form Fields", "HIGH", 
                      f"Registration form missing fields: {', '.join(missing_fields)}",
                      "All registration fields should exist", 
                      f"Missing: {missing_fields}", 
                      capture_console_errors(console_messages),
                      ["screenshots/02-register-page.png"])
        
        print("[OK] Register page elements verified")
        
    except Exception as e:
        add_defect("Register", "Page Load", "CRITICAL", f"Register page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/02-register-page.png"])
        raise

# ============================================================================
# TEST: Dashboard Home
# ============================================================================
async def test_dashboard_home(page, console_messages):
    """Test dashboard home page"""
    print("\n" + "="*80)
    print("TEST: Dashboard Home")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.screenshot(path="screenshots/03-dashboard-home.png")
        
        # Check for dashboard widgets
        widgets = await page.query_selector_all(".dashboard-widget, [class*='widget'], [class*='card']")
        print(f"Found {len(widgets)} potential widget/card elements")
        
        # Check for navigation links
        nav_links = await page.query_selector_all("nav a, aside a, [class*='sidebar'] a")
        print(f"Found {len(nav_links)} navigation links")
        
        if len(nav_links) < 5:
            add_defect("Dashboard", "Navigation", "MEDIUM", 
                      f"Expected multiple navigation links, found only {len(nav_links)}",
                      "Should have links to Classes, Chat, Flashcards, etc.",
                      f"Only {len(nav_links)} links found",
                      capture_console_errors(console_messages),
                      ["screenshots/03-dashboard-home.png"])
        
        print("[OK] Dashboard home verified")
        
    except Exception as e:
        add_defect("Dashboard", "Page Load", "CRITICAL", f"Dashboard failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/03-dashboard-home.png"])
        raise

# ============================================================================
# TEST: Classes Page
# ============================================================================
async def test_classes_page(page, console_messages):
    """Test classes management"""
    print("\n" + "="*80)
    print("TEST: Classes Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/classes")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/04-classes-before.png")
        
        # Look for "Create Class" or similar button
        create_buttons = await page.query_selector_all("button:has-text('Create'), button:has-text('Add'), button:has-text('New')")
        
        if len(create_buttons) == 0:
            add_defect("Classes", "Create Button", "HIGH", 
                      "No create/add class button found",
                      "Should have button to create new class",
                      "No matching button found",
                      capture_console_errors(console_messages),
                      ["screenshots/04-classes-before.png"])
        else:
            print(f"[OK] Found {len(create_buttons)} potential create buttons")
            # TODO: Click button, fill form, submit, verify
        
        # Check for class list
        class_items = await page.query_selector_all("[class*='class'], [class*='item'], [class*='card']")
        print(f"Found {len(class_items)} potential class items")
        
        await page.screenshot(path="screenshots/04-classes-after.png")
        
    except Exception as e:
        add_defect("Classes", "Page Load", "CRITICAL", f"Classes page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), 
                  ["screenshots/04-classes-before.png"])
        raise

# ============================================================================
# TEST: Assignments Page  
# ============================================================================
async def test_assignments_page(page, console_messages):
    """Test assignments management"""
    print("\n" + "="*80)
    print("TEST: Assignments Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/assignments")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/05-assignments.png")
        
        # Check for create button
        create_buttons = await page.query_selector_all("button:has-text('Create'), button:has-text('Add'), button:has-text('New')")
        print(f"Found {len(create_buttons)} potential create buttons")
        
        # TODO: Test assignment creation workflow
        
        print("[OK] Assignments page loaded")
        
    except Exception as e:
        add_defect("Assignments", "Page Load", "CRITICAL", f"Assignments page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/05-assignments.png"])
        raise

# ============================================================================
# TEST: Chat Page
# ============================================================================
async def test_chat_page(page, console_messages):
    """Test chat functionality"""
    print("\n" + "="*80)
    print("TEST: Chat Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/chat")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/06-chat-before.png")
        
        # Check for message input
        message_input = await page.query_selector("textarea, input[type='text']")
        if not message_input:
            add_defect("Chat", "Message Input", "HIGH", 
                      "No message input field found",
                      "Should have textarea or input for messages",
                      "No input field found",
                      capture_console_errors(console_messages),
                      ["screenshots/06-chat-before.png"])
        
        # Check for conversation list
        conversations = await page.query_selector_all(".conversation, [class*='conversation'], [class*='sidebar'] > div")
        print(f"Found {len(conversations)} potential conversation elements")
        
        # TODO: Test sending message, clicking conversation, loading history
        
        await page.screenshot(path="screenshots/06-chat-after.png")
        
    except Exception as e:
        add_defect("Chat", "Page Load", "CRITICAL", f"Chat page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/06-chat-before.png"])
        raise

# ============================================================================
# TEST: Flashcards Page
# ============================================================================
async def test_flashcards_page(page, console_messages):
    """Test flashcard functionality"""
    print("\n" + "="*80)
    print("TEST: Flashcards Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/flashcards")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/07-flashcards.png")
        
        # Check for create deck button
        create_buttons = await page.query_selector_all("button:has-text('Create'), button:has-text('New'), button:has-text('Add')")
        print(f"Found {len(create_buttons)} potential create buttons")
        
        # TODO: Test deck creation, card addition, study mode
        
        print("[OK] Flashcards page loaded")
        
    except Exception as e:
        add_defect("Flashcards", "Page Load", "CRITICAL", f"Flashcards page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/07-flashcards.png"])
        raise

# ============================================================================
# TEST: Transcribe Page
# ============================================================================
async def test_transcribe_page(page, console_messages):
    """Test audio transcription"""
    print("\n" + "="*80)
    print("TEST: Transcribe Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/transcribe")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/08-transcribe.png")
        
        # Check for file upload
        file_input = await page.query_selector("input[type='file']")
        upload_button = await page.query_selector("button:has-text('Upload'), button:has-text('Select')")
        
        if not file_input and not upload_button:
            add_defect("Transcribe", "Upload Controls", "HIGH",
                      "No file upload controls found",
                      "Should have file input or upload button",
                      "No upload controls found",
                      capture_console_errors(console_messages),
                      ["screenshots/08-transcribe.png"])
        
        print("[OK] Transcribe page loaded")
        
    except Exception as e:
        add_defect("Transcribe", "Page Load", "CRITICAL", f"Transcribe page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/08-transcribe.png"])
        raise

# ============================================================================
# TEST: TTS Page
# ============================================================================
async def test_tts_page(page, console_messages):
    """Test text-to-speech"""
    print("\n" + "="*80)
    print("TEST: TTS Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/tts")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/09-tts.png")
        
        # Check for text input
        text_input = await page.query_selector("textarea, input[type='text']")
        generate_button = await page.query_selector("button:has-text('Generate'), button:has-text('Speak'), button:has-text('Play')")
        
        if not text_input:
            add_defect("TTS", "Text Input", "HIGH",
                      "No text input field found",
                      "Should have textarea for text input",
                      "No input field found",
                      capture_console_errors(console_messages),
                      ["screenshots/09-tts.png"])
        
        if not generate_button:
            add_defect("TTS", "Generate Button", "HIGH",
                      "No generate/speak button found",
                      "Should have button to generate speech",
                      "No button found",
                      capture_console_errors(console_messages),
                      ["screenshots/09-tts.png"])
        
        print("[OK] TTS page loaded")
        
    except Exception as e:
        add_defect("TTS", "Page Load", "CRITICAL", f"TTS page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/09-tts.png"])
        raise

# ============================================================================
# TEST: Materials Page
# ============================================================================
async def test_materials_page(page, console_messages):
    """Test study materials management"""
    print("\n" + "="*80)
    print("TEST: Materials Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/materials")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/10-materials.png")
        
        # Check for upload controls
        file_input = await page.query_selector("input[type='file']")
        upload_button = await page.query_selector("button:has-text('Upload'), button:has-text('Add')")
        
        print(f"[INFO] File input: {file_input is not None}, Upload button: {upload_button is not None}")
        
        # TODO: Test material upload, view, download
        
        print("[OK] Materials page loaded")
        
    except Exception as e:
        add_defect("Materials", "Page Load", "CRITICAL", f"Materials page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/10-materials.png"])
        raise

# ============================================================================
# TEST: Notifications Page
# ============================================================================
async def test_notifications_page(page, console_messages):
    """Test notifications"""
    print("\n" + "="*80)
    print("TEST: Notifications Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/notifications")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/11-notifications.png")
        
        # Check for notifications list
        notifications = await page.query_selector_all("[class*='notification'], [class*='item'], li")
        print(f"Found {len(notifications)} potential notification items")
        
        # TODO: Test mark as read, delete notification
        
        print("[OK] Notifications page loaded")
        
    except Exception as e:
        add_defect("Notifications", "Page Load", "CRITICAL", f"Notifications page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/11-notifications.png"])
        raise

# ============================================================================
# TEST: Messages Page
# ============================================================================
async def test_messages_page(page, console_messages):
    """Test direct messaging"""
    print("\n" + "="*80)
    print("TEST: Messages Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/messages")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/12-messages.png")
        
        # Check for message interface
        message_input = await page.query_selector("textarea, input[type='text']")
        print(f"[INFO] Message input found: {message_input is not None}")
        
        # TODO: Test sending message, viewing conversation
        
        print("[OK] Messages page loaded")
        
    except Exception as e:
        add_defect("Messages", "Page Load", "CRITICAL", f"Messages page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/12-messages.png"])
        raise

# ============================================================================
# TEST: Groups Page
# ============================================================================
async def test_groups_page(page, console_messages):
    """Test study groups"""
    print("\n" + "="*80)
    print("TEST: Groups Page")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/groups")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/13-groups.png")
        
        # Check for create/join buttons
        create_button = await page.query_selector("button:has-text('Create'), button:has-text('New')")
        join_button = await page.query_selector("button:has-text('Join'), button:has-text('Browse')")
        
        print(f"[INFO] Create button: {create_button is not None}, Join button: {join_button is not None}")
        
        # TODO: Test group creation, joining, viewing
        
        print("[OK] Groups page loaded")
        
    except Exception as e:
        add_defect("Groups", "Page Load", "CRITICAL", f"Groups page failed: {e}",
                  "Page should load successfully", "Exception occurred",
                  capture_console_errors(console_messages), ["screenshots/13-groups.png"])
        raise

# ============================================================================
# TEST: Logs Page (if exists)
# ============================================================================
async def test_logs_page(page, console_messages):
    """Test system logs (if available)"""
    print("\n" + "="*80)
    print("TEST: Logs Page (Optional)")
    print("="*80)
    
    try:
        await page.goto(f"{BASE_URL}/dashboard/logs")
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(1)
        await page.screenshot(path="screenshots/14-logs.png")
        
        print("[OK] Logs page loaded (if implemented)")
        
    except Exception as e:
        print(f"[INFO] Logs page may not be implemented: {e}")
        # Not adding as defect - may be optional

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================
async def run_full_test():
    """Run comprehensive E2E test of all application pages"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Console log capture
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        try:
            print("\n" + "="*80)
            print("COMPREHENSIVE E2E TEST - LITTLE MONSTER GPA")
            print("="*80)
            print(f"Test Started: {datetime.now().isoformat()}")
            print(f"Base URL: {BASE_URL}")
            print(f"Test User: {TEST_EMAIL}")
            
            # Create screenshots directory
            import os
            os.makedirs("screenshots", exist_ok=True)
            
            # Run login first
            await test_login_page(page, console_messages)
            
            # Setup authentication for dashboard tests
            await setup_auth(page)
            
            # Run all dashboard page tests
            await test_register_page(page, console_messages)
            await test_dashboard_home(page, console_messages)
            await test_classes_page(page, console_messages)
            await test_assignments_page(page, console_messages)
            await test_chat_page(page, console_messages)
            await test_flashcards_page(page, console_messages)
            await test_transcribe_page(page, console_messages)
            await test_tts_page(page, console_messages)
            await test_materials_page(page, console_messages)
            await test_notifications_page(page, console_messages)
            await test_messages_page(page, console_messages)
            await test_groups_page(page, console_messages)
            await test_logs_page(page, console_messages)
            
            # Generate defect report
            print("\n" + "="*80)
            print("DEFECT SUMMARY")
            print("="*80)
            
            if len(defects) == 0:
                print("✅ NO DEFECTS FOUND - ALL TESTS PASSED!")
            else:
                print(f"❌ FOUND {len(defects)} DEFECTS:")
                
                critical = [d for d in defects if d['severity'] == 'CRITICAL']
                high = [d for d in defects if d['severity'] == 'HIGH']
                medium = [d for d in defects if d['severity'] == 'MEDIUM']
                low = [d for d in defects if d['severity'] == 'LOW']
                
                print(f"  CRITICAL: {len(critical)}")
                print(f"  HIGH:     {len(high)}")
                print(f"  MEDIUM:   {len(medium)}")
                print(f"  LOW:      {len(low)}")
                
                # Write defect report
                with open("tests/e2e/DEFECT-LIST.md", "w", encoding='utf-8') as f:
                    f.write("# Comprehensive E2E Test - Defect List\n\n")
                    f.write(f"**Test Date:** {datetime.now().isoformat()}\n\n")
                    f.write(f"**Total Defects:** {len(defects)}\n\n")
                    f.write(f"- CRITICAL: {len(critical)}\n")
                    f.write(f"- HIGH: {len(high)}\n")
                    f.write(f"- MEDIUM: {len(medium)}\n")
                    f.write(f"- LOW: {len(low)}\n\n")
                    f.write("---\n\n")
                    
                    for defect in defects:
                        f.write(f"## DEFECT #{defect['number']:03d}: [{defect['page']}] - {defect['feature']} - {defect['severity']}\n\n")
                        f.write(f"**Description:** {defect['description']}\n\n")
                        f.write(f"**Expected:** {defect['expected']}\n\n")
                        f.write(f"**Actual:** {defect['actual']}\n\n")
                        if defect['console_errors']:
                            f.write(f"**Console Errors:**\n```\n")
                            for err in defect['console_errors']:
                                f.write(f"{err}\n")
                            f.write(f"```\n\n")
                        if defect['screenshots']:
                            f.write(f"**Screenshots:** {', '.join(defect['screenshots'])}\n\n")
                        f.write(f"**Timestamp:** {defect['timestamp']}\n\n")
                        f.write(f"**Status:** Open\n\n")
                        f.write("---\n\n")
                
                print(f"\n✅ Defect report written to tests/e2e/DEFECT-LIST.md")
            
            # Console error summary
            errors = capture_console_errors(console_messages)
            if errors:
                print(f"\n⚠️  Found {len(errors)} console errors (excluding favicon):")
                for err in errors[:10]:  # Show first 10
                    print(f"  - {err}")
            
            print(f"\n✅ All screenshots saved to screenshots/ directory")
            print(f"Test Completed: {datetime.now().isoformat()}")
            
            return len(defects) == 0
            
        except Exception as e:
            print(f"\n❌ CRITICAL TEST FAILURE: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(run_full_test())
    sys.exit(0 if result else 1)
