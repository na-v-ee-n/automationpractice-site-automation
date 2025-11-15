import pytest
import allure
from pages.registration_page import RegistrationPage
from utils.excel_reader import read_test_data

@allure.feature("User Registration")
@allure.story("Account Creation")
@pytest.mark.usefixtures("setup")
class TestRegistration:
    @allure.title("Registration Test - {data[Email]}")
    @allure.description("Test user registration functionality with different data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data("Login Testcases.xlsx", "Registration"))
    def test_registration_cases(self, data):
        with allure.step("Initialize registration page"):
            page = RegistrationPage(self.driver)
        
        with allure.step(f"Register with email: {data['Email']}"):
            allure.attach(data["Email"], "Email", allure.attachment_type.TEXT)
            allure.attach(data["Password"], "Password", allure.attachment_type.TEXT)
            page.register(data["Email"], data["Password"])
        
        with allure.step("Verify registration result"):
            expected = data["ExpectedResult"]
            try:
                if "success" in expected.lower():
                    assert page.is_registration_successful(), f"Expected success for {data}"
                else:
                    assert expected.lower() in page.get_error_message().lower(), f"Expected error for {data}"
            except Exception as e:
                from utils.test_helper import attach_on_failure
                attach_on_failure(self.driver)
                raise e
