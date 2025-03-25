import re
from playwright.sync_api import Playwright, sync_playwright, expect

def test_OpenRoles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.bamfunds.com/")
        page.get_by_label("Header").get_by_role("link", name="Career").hover()
        with page.expect_popup() as page1_info:
            page.get_by_label("Header").get_by_role("link", name="Open Roles").click()
        page1 = page1_info.value
        page1.wait_for_load_state("domcontentloaded")  # Ensure the popup page is loaded

        # Wait for the specific element to be visible before clicking
        page1.locator("a").filter(has_text="REQ6737 | New York | Posted").wait_for(state="visible")
        page1.locator("a").filter(has_text="REQ6737 | New York | Posted").click()

        # Wait for the next page to load
        page1.wait_for_load_state("domcontentloaded")

        # Wait for the specific link to be visible before clicking
        page1.locator("a").filter(has_text="Full-Stack Engineer, Equity").wait_for(state="visible")
        page1.locator("a").filter(has_text="Full-Stack Engineer, Equity").click()

        # Wait for the apply button to be visible and enabled
        page1.get_by_role("button", name="Apply now").wait_for(state="visible")
        page1.get_by_role("button", name="Apply now").click()

        # Wait for the final heading to be visible
        page1.get_by_role("heading", name="Start your application").wait_for(state="visible")
        page1.get_by_role("heading", name="Start your application").click()

        context.close()
        browser.close()