from playwright.sync_api import sync_playwright
import os
from datetime import datetime


def test_founders():
    # Setup screenshot directory
    os.makedirs("reports/screenshots", exist_ok=True)
    screenshot_path = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://www.bamfunds.com")

            # Close cookie popup if it exists
            if page.locator('button.cookie-button').is_visible():
                page.locator('button.cookie-button').click()

            # Hover over "About Us" (triggers dropdown)
            page.get_by_label("Header").get_by_role("link", name="About Us").hover()

            # Now click "Leadership" (visible after hover)
            page.get_by_label("Header").get_by_role("link", name="Leadership").click()

            # Click a specific leadership profile
            page.get_by_role("link", name="Leadership Headshot Dmitry").click()

            # Verify the founder's name
            founder_name_1 = page.get_by_text("Dmitry Balyasny", exact=True).inner_text()
            assert founder_name_1 == "Dmitry Balyasny"

            founder_name_2 = page.get_by_text("Taylor O'Malley", exact=True).inner_text()
            assert founder_name_2 == "Taylor O'Malley"

            founder_name_3 = page.get_by_text("Scott Schroeder", exact=True).inner_text()
            assert founder_name_3 == "Scott Schroeder"

        except AssertionError as e:
            # Take screenshot on assertion failure
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"reports/screenshots/test_founders_failed_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            raise e
        finally:
            browser.close()