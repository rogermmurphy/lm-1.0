#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test: Chat History Display
Tests that clicking a conversation loads and displays historical messages
"""
import asyncio
from playwright.async_api import async_playwright
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

async def test_chat_history():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Listen to console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        try:
            print("\n" + "="*80)
            print("CHAT HISTORY E2E TEST - PORT 3000")
            print("="*80)
            
            # Step 1: Navigate to login
            print("\n[1] Navigating to login...")
            await page.goto("http://localhost:3000/login")
            await page.wait_for_load_state("networkidle")
            
            # Step 2: Login
            print("[2] Logging in as test@test.com...")
            await page.fill("#email", "test@test.com")
            await page.fill("#password", "Test1234!")
            await page.click("button[type='submit']")
            await page.wait_for_url("**/dashboard**", timeout=10000)
            print("[OK] Logged in successfully")
            
            # Step 3: Set localStorage to skip onboarding modal
            print("\n[3] Setting localStorage to skip onboarding modal...")
            await page.evaluate("localStorage.setItem('hasSeenOnboarding', 'true')")
            
            # Step 3.5: Navigate to chat
            print("[3.5] Navigating to chat page...")
            await page.goto("http://localhost:3000/dashboard/chat")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(1)  # Wait for React to render
            
            # Step 4: Take screenshot before clicking
            print("[4] Taking screenshot of chat page...")
            await page.screenshot(path="chat-before-click.png")
            
            # Step 5: Click first conversation
            print("\n[5] Clicking first conversation in sidebar...")
            conversations = await page.query_selector_all(".w-64 .space-y-1 > div")
            if len(conversations) == 0:
                print("[FAIL] No conversations found in sidebar")
                return False
            
            print(f"Found {len(conversations)} conversations")
            await conversations[0].click()
            await asyncio.sleep(2)  # Wait for async loading
            
            # Step 6: Take screenshot after clicking
            print("[6] Taking screenshot after clicking...")
            await page.screenshot(path="chat-after-click.png")
            
            # Step 7: Check for messages in DOM
            print("\n[7] Checking if messages rendered...")
            messages_div = await page.query_selector(".flex-1.overflow-y-auto")
            if not messages_div:
                print("[FAIL] Messages container not found")
                return False
            
            # Check for message bubbles (user/assistant)
            message_bubbles = await page.query_selector_all(".rounded-lg.px-4.py-3")
            message_count = len(message_bubbles)
            print(f"Found {message_count} message bubbles in DOM")
            
            # Step 8: Print console logs
            print("\n[8] Console logs:")
            print("-" * 60)
            chat_logs = [msg for msg in console_messages if '[Chat]' in msg]
            if chat_logs:
                for log in chat_logs:
                    print(log)
            else:
                print("[WARN] No [Chat] debug logs found")
            
            # Print all console logs
            print("\nAll console output:")
            for msg in console_messages[-20:]:  # Last 20 messages
                print(msg)
            
            # Step 9: Verify results
            print("\n" + "="*80)
            print("TEST RESULTS")
            print("="*80)
            
            if message_count > 0:
                print(f"[PASS] {message_count} messages displayed")
                errors = [msg for msg in console_messages if 'error' in msg.lower() and 'favicon' not in msg.lower()]
                if errors:
                    print(f"\n[WARN] Errors found ({len(errors)}):")
                    for err in errors:
                        print(f"  - {err}")
                    return False
                return True
            else:
                print("[FAIL] No messages displayed")
                return False
                
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    result = asyncio.run(test_chat_history())
    sys.exit(0 if result else 1)
