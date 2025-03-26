import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="function")
def page(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def test_forgotpsd(page, request):
    """Test password recovery flow with HTML reporting"""
    # Setup reporting directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports/screenshots", exist_ok=True)

    # Store test metadata for HTML report
    test_name = request.node.name
    report_data = {
        "test_name": test_name,
        "steps": [],
        "screenshots": []
    }

    def capture_step(step_name, page_obj):
        """Helper function to capture steps and screenshots"""
        screenshot_path = f"reports/screenshots/{test_name}_{step_name}_{timestamp}.png"
        page_obj.screenshot(path=screenshot_path, full_page=True)
        report_data["steps"].append(step_name)
        report_data["screenshots"].append(screenshot_path)
        return screenshot_path

    try:
        # --- Main test flow ---
        page.goto("https://www.bamfunds.com/", timeout=60000)
        capture_step("main_page_loaded", page)

        # First popup - Investor Login
        with page.expect_popup(timeout=15000) as page1_info:
            page.get_by_role("link", name="Investor Login").click()
        page1 = page1_info.value
        capture_step("investor_login_popup", page1)

        page1.get_by_text("Sign in with Okta").click()
        capture_step("okta_signin_clicked", page1)

        # Wait for username field and fill it
        page1.get_by_role("textbox", name="Username").fill("lucas")
        capture_step("username_filled", page1)

        # Wait for Next button to be enabled before clicking
        next_button = page1.get_by_role("button", name="Next")
        expect(next_button).to_be_enabled(timeout=10000)
        next_button.click()
        capture_step("next_button_clicked", page1)

        # Forgot password flow
        page1.get_by_role("link", name="Forgot password?").click()
        capture_step("forgot_password_clicked", page1)

        # Verification
        expect(page1.get_by_text("Reset password is not allowed")).to_be_visible(timeout=10000)
        capture_step("verification_complete", page1)

        # Attach data to HTML report
        pytest_html = request.config.pluginmanager.getplugin("html")
        extra = []
        for i, step in enumerate(report_data["steps"]):
            extra.append(pytest_html.extras.html(f"<h3>Step {i + 1}: {step}</h3>"))
            extra.append(pytest_html.extras.image(report_data["screenshots"][i]))

        request.node.extra = extra

    except Exception as e:
        # Capture final screenshot on failure
        capture_step("test_failed", page1 if 'page1' in locals() else page)
        raise e
