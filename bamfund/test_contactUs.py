import re
from playwright.sync_api import sync_playwright, expect
import os
from datetime import datetime


def test_ContactUS():
    # Setup screenshot directory
    os.makedirs("reports/screenshots", exist_ok=True)
    screenshot_path = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto("https://www.bamfunds.com/")
            page.get_by_role("button", name="Accept cookies").click()
            page.get_by_role("link", name="Contact Us").click()

            page.get_by_role("textbox", name="First Name*").click()
            page.get_by_role("button", name="Submit").click()
            assert page.locator("div").filter(has_text=re.compile(r"^First Name\*This field is required$")).is_visible()

            page.get_by_role("textbox", name="Last Name*").click()
            assert page.locator("div").filter(has_text=re.compile(r"^Last Name\*This field is required$")).is_visible()

            page.get_by_role("textbox", name="E-mail Address*").click()
            assert page.locator("div").filter(
                has_text=re.compile(r"^E-mail Address\*This field is required$")).is_visible()

            page.get_by_role("textbox", name="Phone Number").click()
            page.get_by_role("textbox", name="Phone Number").fill("12")
            assert page.get_by_text("Invalid phone number").is_visible()

            page.get_by_role("textbox", name="Your Message*").click()
            assert page.locator("div").filter(
                has_text=re.compile(r"^Your Message\*This field is required$")).is_visible()

        except AssertionError as e:
            # Take screenshot on assertion failure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"reports/screenshots/test_ContactUS_failed_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            raise e
        finally:
            context.close()
            browser.close()