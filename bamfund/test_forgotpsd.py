import re
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, expect


def test_forgotpsd():
    """Test password recovery flow with reporting"""
    # Setup reporting directory
    os.makedirs("reports/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # --- Your original test code starts ---
            page.goto("https://www.bamfunds.com/")
            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="Investor Login").click()
            page1 = page1_info.value
            page1.get_by_text("Sign in with Okta").click()
            page1.close()
            with page.expect_popup() as page2_info:
                page.get_by_role("link", name="Investor Login").click()
            page2 = page2_info.value
            page2.get_by_text("Sign in with Okta").click()
            page2.get_by_role("link", name="Go to Homepage").click()
            # --- Your original test code ends ---

        except Exception as e:
            # Capture screenshots on failure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"reports/screenshots/main_failed_{timestamp}.png", full_page=True)
            if 'page1' in locals():
                page1.screenshot(path=f"reports/screenshots/popup1_failed_{timestamp}.png", full_page=True)
            if 'page2' in locals():
                page2.screenshot(path=f"reports/screenshots/popup2_failed_{timestamp}.png", full_page=True)
            raise
        finally:
            context.close()
            browser.close()


