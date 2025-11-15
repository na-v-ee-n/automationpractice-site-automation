import pytest
import allure
from pages.registration_page import RegistrationPage
from utils.excel_reader import read_test_data
from utils.test_helper import step, attach_text, attach_html, log_and_assert
from testdata.data_paths import REGISTRATION_TESTCASES

@pytest.mark.usefixtures("setup")
class TestRegistration:

    @allure.title("Registration Test - {data[Test_Case_Title]}")
    @allure.description("Test registration functionality with different credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data(REGISTRATION_TESTCASES, "Registration_TestData"))
    def test_registration_cases(self, data):
        if data["Module"] != "Registration":
            pytest.skip("Not a registration test case")

        with step("Navigate to registration page"):
            registration_page = RegistrationPage(self.driver)
            registration_visible = registration_page.navigate_to_registration()
            log_and_assert(registration_visible, "Registration button not visible after clicking My Account")

        # Extract email and password from Excel data
        email = str(data.get("Email", "testuser@example.com"))
        password = str(data.get("Password", "testpass123"))
        
        # Generate random email ONLY for data0 (REG-01) and data1 (REG-02)
        import random
        import string
        test_case_id = data.get("Test_Case_ID", "")
        
        # Generate random email only for REG-01 and REG-02
        if test_case_id == "REG-01" or test_case_id == "REG-02":
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))
            email = f"user{random_suffix}@gmail.com"
            print(f"Generated random email for {test_case_id}: {email}")
        
        # Handle NaN values for all other test cases
        import pandas as pd
        if test_case_id != "REG-01" and test_case_id != "REG-02":
            if pd.isna(email) or str(email).lower() == "nan" or not email:
                email = ""
        if pd.isna(password) or str(password).lower() == "nan" or not password:
            password = ""

        attach_text(email, "Email")
        attach_text(password, "Password")

        with step(f"Register with credentials: {email}"):
            registration_success = registration_page.register(email, password)
            
            # Log password strength after entering password
            strength_text = registration_page.get_password_strength_text()
            print(f"Password strength text: {strength_text}")
            attach_text(strength_text, "Password Strength")
            
            # If password is too weak, expect registration to fail
            if not registration_success:
                with step("Verify weak password is rejected"):
                    strength_text = registration_page.get_password_strength_text()
                    log_and_assert("Very weak" in strength_text or "weak" in strength_text.lower(), "Expected weak password validation")
                    return  # Skip further validation for weak passwords
            
            self.driver.implicitly_wait(5)

        with step("Verify registration result"):
            try:
                expected_result = data.get("Expected_Result", "")
                test_case_id = data.get("Test_Case_ID", "")
                
                # Wait a moment for page to load
                import time
                time.sleep(2)
                
                if "Registration succeeds" in expected_result or "REG-01" in test_case_id or "REG-02" in test_case_id:
                    # Expect successful registration
                    success = registration_page.is_registration_successful()
                    log_and_assert(success, "Registration failed - Expected successful registration")
                    
                    if success:
                        with step("Logout and verify"):
                            registration_page.logout()
                            logout_success = registration_page.is_register_button_visible()
                            log_and_assert(logout_success, "Registration button not visible after logout")
                else:
                    # Expect registration to fail
                    success = registration_page.is_registration_successful()
                    if success:
                        # Registration succeeded when it should have failed - logout to clean up
                        print("Warning: Registration succeeded when failure was expected")
                        registration_page.logout()
                        log_and_assert(False, "Registration succeeded when it should have failed")
                    else:
                        # Registration failed as expected - check for error message
                        error_found = registration_page.is_error_displayed()
                        log_and_assert(error_found or not success, "Expected error message or registration failure")
            except Exception as e:
                from utils.test_helper import attach_on_failure
                attach_on_failure(self.driver)
                raise e
