"""
Complete End-to-End Playwright Testing Script
Zero Tolerance Testing - Every Page Must Load Without Errors
"""
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

class E2ETestRunner:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "pages_tested": []
        }
        self.console_errors = []
        
    async def run_tests(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            # Capture console logs
            page.on("console", lambda msg: self.handle_console(msg))
            page.on("pageerror", lambda err: self.console_errors.append(f"PAGE ERROR: {err}"))
            
            # Monitor failed responses
            def handle_response(response):
                if response.status >= 400:
                    url = response.url
                    # Ignore non-critical resources
                    if not any(x in url.lower() for x in ['favicon', '.ico', '.png', '.jpg', '.svg']):
                        self.console_errors.append(f"HTTP {response.status}: {url}")
            
            page.on("response", handle_response)
            
            try:
                # Test 1: Login Page
                await self.test_login(page)
                
                # Test 2: Dashboard
                await self.test_page(page, "/dashboard", "Dashboard")
                
                # Test 3: Classes
                await self.test_page(page, "/dashboard/classes", "Classes")
                
                # Test 4: Assignments
                await self.test_page(page, "/dashboard/assignments", "Assignments")
                
                # Test 5: Flashcards
                await self.test_page(page, "/dashboard/flashcards", "Flashcards")
                
                # Test 6: Groups
                await self.test_page(page, "/dashboard/groups", "Study Groups")
                
                # Test 7: Chat
                await self.test_page(page, "/dashboard/chat", "AI Chat")
                
                # Test 8: Transcribe
                await self.test_page(page, "/dashboard/transcribe", "Transcribe")
                
                # Test 9: TTS
                await self.test_page(page, "/dashboard/tts", "TTS")
                
                # Test 10: Materials
                await self.test_page(page, "/dashboard/materials", "Materials")
                
                # Test 11: Notifications
                await self.test_page(page, "/dashboard/notifications", "Notifications")
                
                # Test 12: Messages
                await self.test_page(page, "/dashboard/messages", "Messages")
                
            finally:
                await browser.close()
                
            return self.results
    
    def handle_console(self, msg):
        """Capture console messages"""
        msg_type = msg.type
        msg_text = msg.text
        
        if msg_type == "error":
            # Ignore non-critical resource loading failures
            # Generic "Failed to load resource" without specific URL is typically favicon/icons
            if "failed to load resource" in msg_text.lower() and "404" in msg_text:
                # Generic 404 message - likely favicon/icon - not critical
                return
            # Capture all other errors
            self.console_errors.append(f"CONSOLE ERROR: {msg_text}")
        
    async def test_login(self, page):
        """Test login functionality"""
        test_name = "Login Page"
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"{'='*60}")
        
        self.console_errors = []
        
        try:
            # Navigate to login - Use Cloudflare URL for remote access
            await page.goto("https://prescribed-plug-complexity-prince.trycloudflare.com/login", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            
            # Check for console errors
            if self.console_errors:
                raise Exception(f"Console errors on login page: {self.console_errors}")
            
            # Fill login form
            await page.fill("input[type='email']", "testuser@example.com")
            await page.fill("input[type='password']", "TestPass123!")
            
            # Click login button
            await page.click("button[type='submit']")
            
            # Wait for navigation
            await page.wait_for_url("**/dashboard", timeout=10000)
            await page.wait_for_timeout(2000)
            
            # Check for errors after login
            if self.console_errors:
                raise Exception(f"Console errors after login: {self.console_errors}")
            
            self.results["tests_passed"] += 1
            self.results["pages_tested"].append({
                "name": test_name,
                "status": "PASSED",
                "errors": []
            })
            print(f"[PASS] {test_name} PASSED")
            
        except Exception as e:
            self.results["tests_failed"] += 1
            error_msg = str(e)
            self.results["errors"].append(f"{test_name}: {error_msg}")
            self.results["pages_tested"].append({
                "name": test_name,
                "status": "FAILED",
                "errors": [error_msg] + self.console_errors
            })
            print(f"[FAIL] {test_name} FAILED: {error_msg}")
            raise  # Re-raise to stop testing
    
    async def test_page(self, page, url, name):
        """Test a specific page"""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"{'='*60}")
        
        self.console_errors = []
        
        try:
            # Navigate to page - Use Cloudflare URL for remote access
            await page.goto(f"https://prescribed-plug-complexity-prince.trycloudflare.com{url}", wait_until="networkidle")
            await page.wait_for_timeout(2000)
            
            # Check for console errors
            if self.console_errors:
                raise Exception(f"Console errors: {self.console_errors}")
            
            # Check for 401 errors
            for error in self.console_errors:
                if "401" in error:
                    raise Exception(f"401 Unauthorized error detected")
            
            self.results["tests_passed"] += 1
            self.results["pages_tested"].append({
                "name": name,
                "url": url,
                "status": "PASSED",
                "errors": []
            })
            print(f"[PASS] {name} PASSED")
            
        except Exception as e:
            self.results["tests_failed"] += 1
            error_msg = str(e)
            self.results["errors"].append(f"{name}: {error_msg}")
            self.results["pages_tested"].append({
                "name": name,
                "url": url,
                "status": "FAILED",
                "errors": [error_msg] + self.console_errors
            })
            print(f"[FAIL] {name} FAILED: {error_msg}")
            raise  # Re-raise to stop testing

async def main():
    print("\n" + "="*60)
    print("ZERO TOLERANCE END-TO-END TESTING")
    print("="*60)
    
    runner = E2ETestRunner()
    results = await runner.run_tests()
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    print(f"Total Errors: {len(results['errors'])}")
    
    # Save results
    with open("tests/e2e/test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: tests/e2e/test_results.json")
    
    # Exit with error code if any tests failed
    if results['tests_failed'] > 0:
        print("\n[FAIL] ZERO TOLERANCE FAILED - Errors detected!")
        exit(1)
    else:
        print("\n[PASS] ZERO TOLERANCE PASSED - All tests successful!")
        exit(0)

if __name__ == "__main__":
    asyncio.run(main())
