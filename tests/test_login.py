import pytest
import allure
import logging
from pages.login_page import LoginPage
from utils.excel_reader import read_test_data
from utils.test_helper import step, attach_text, attach_html, log_and_assert
from testdata.data_paths import LOGIN_TESTCASES

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("setup")
class TestLogin:

    @allure.title("Login Test - {data[Test Case Title]}")
    @allure.description("Test login functionality with different credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data(LOGIN_TESTCASES, "Sheet1"))
    def test_login_cases(self, data):
        if data["Module"] != "Login":
            pytest.skip("Not a login test case")

        with step("Navigate to login page"):
            logger.info(f"Starting test: {data['Test Case Title']}")
            login_page = LoginPage(self.driver)
            logger.info("Navigating to login page")
            login_visible = login_page.navigate_to_login()
            log_and_assert(login_visible, "Login button not visible after clicking My Account")
            logger.info("Login page loaded successfully")

        # Extract email and password from Test Data
        test_data = str(data.get("Test Data", ""))
        try:
            if "email" in test_data.lower() and "password" in test_data.lower():
                parts = test_data.split(" ")
                email = parts[1] if len(parts) > 1 else "testuser@example.com"
                password = parts[3] if len(parts) > 3 else "testpass123"
            else:
                email = "testuser@example.com"
                password = "testpass123"
        except (IndexError, AttributeError):
            email = "testuser@example.com"
            password = "testpass123"

        attach_text(email, "Email")
        attach_text(password, "Password")
        logger.info(f"Using credentials - Email: {email}")

        with step(f"Login with credentials: {email}"):
            logger.info("Entering credentials and clicking login")
            login_page.login(email, password)
            self.driver.implicitly_wait(5)

        with step("Verify login result"):
            try:
                if "Login succeeds" in data["Expected Result"]:
                    logger.info("Verifying successful login")
                    success = login_page.is_login_successful()
                    log_and_assert(success, "Logout button not found - Login failed")
                    logger.info("Login successful")
                    
                    with step("Logout and verify"):
                        logger.info("Logging out")
                        login_page.logout()
                        logout_success = login_page.is_login_button_visible()
                        log_and_assert(logout_success, "Login button not visible after logout")
                        logger.info("Logout successful")
                else:
                    logger.info("Verifying login failure")
                    error_found = login_page.is_error_displayed()
                    log_and_assert(error_found, "Expected error message not found")
                    logger.info("Error message displayed as expected")
            except Exception as e:
                from utils.test_helper import attach_on_failure
                attach_on_failure(self.driver)
                raise e