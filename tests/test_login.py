import pytest
import allure
import os
from pages.login_page import LoginPage
from utils.excel_reader import read_test_data
from utils.test_helper import step, attach_text, attach_html, log_and_assert

# Correct path for Excel file
file_path = os.path.join(os.path.dirname(__file__), "..", "Login Testcases.xlsx")

@pytest.mark.usefixtures("setup")
class TestLogin:

    @allure.title("Login Test - {data[Test Case Title]}")
    @allure.description("Test login functionality with different credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data(file_path, "Sheet1"))
    def test_login_cases(self, data):
        if data["Module"] != "Login":
            pytest.skip("Not a login test case")

        with step("Navigate to login page"):
            login_page = LoginPage(self.driver)
            login_visible = login_page.navigate_to_login()
            log_and_assert(login_visible, "Login button not visible after clicking My Account")

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

        with step(f"Login with credentials: {email}"):
            login_page.login(email, password)
            self.driver.implicitly_wait(5)

        with step("Verify login result"):
            try:
                if "Login succeeds" in data["Expected Result"]:
                    success = login_page.is_login_successful()
                    log_and_assert(success, "Logout button not found - Login failed")
                    
                    with step("Logout and verify"):
                        login_page.logout()
                        logout_success = login_page.is_login_button_visible()
                        log_and_assert(logout_success, "Login button not visible after logout")
                else:
                    error_found = login_page.is_error_displayed()
                    log_and_assert(error_found, "Expected error message not found")
            except Exception as e:
                from utils.test_helper import attach_on_failure
                attach_on_failure(self.driver)
                raise e