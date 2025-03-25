import re
from playwright.sync_api import sync_playwright, expect

def test_invalidLogin():
    # Configure browser with basic settings
    browser = sync_playwright().start().chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Main test flow
    page.goto("https://www.bamfunds.com/")

    # Handle login popup
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Investor Login").click()
    page1 = page1_info.value

    # Okta login steps
    page1.get_by_text("Sign in with Okta").click()
    page1.get_by_role("textbox", name="Username").fill("lucas")
    page1.get_by_text("Keep me signed in").click()
    page1.get_by_role("button", name="Next").click()
    page1.get_by_role("textbox", name="Password").fill("lucas")
    page1.get_by_role("button", name="Verify").click()

    # Verification
    expect(page1.get_by_text("Unable to sign in")).to_be_visible()

    # Cleanup
    context.close()
    browser.close()