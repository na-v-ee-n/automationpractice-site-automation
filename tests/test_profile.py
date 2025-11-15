import pytest
import allure
import logging
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from utils.excel_reader import read_test_data
from utils.test_helper import step, attach_text, log_and_assert
from testdata.data_paths import PROFILE_TESTCASES

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("setup")
class TestProfile:

    @allure.title("Profile Test - {data[Test Case Title]}")
    @allure.description("Test profile address functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data(PROFILE_TESTCASES, "Sheet1"))
    def test_profile_address(self, data):
        if data["Module"] != "Profile":
            pytest.skip("Not a profile test case")

        login_page = LoginPage(self.driver)
        
        if "Persistence" in data["Test Case Title"]:
            with step("Add valid address"):
                logger.info("Starting address persistence test")
                if not login_page.is_login_successful():
                    logger.info("Navigating to login page")
                    login_page.navigate_to_login()
                    logger.info("Logging in with credentials")
                    login_page.login("user123@mail.com", "Str0ngPass!")
                profile_page = ProfilePage(self.driver)
                logger.info("Navigating to addresses")
                profile_page.navigate_to_addresses()
                logger.info("Clicking edit address")
                profile_page.click_edit_address()
                logger.info("Filling address details")
                profile_page.fill_address("Test", "User", "Test Company", "testuser@example.com", 
                                         "9876543210", "123 Main St", "", "Chennai", "Chennai", "110001", "India", False)
                logger.info("Saving address")
                profile_page.save_address()
                log_and_assert(profile_page.is_success_message_displayed(), "Address save failed")
                logger.info("Address saved successfully")
            
            with step("Logout"):
                logger.info("Logging out")
                login_page.logout()
                log_and_assert(login_page.is_login_button_visible(), "Logout failed")
                logger.info("Logout successful")
            
            with step("Login again"):
                logger.info("Logging in again")
                login_page.login("user123@mail.com", "Str0ngPass!")
                log_and_assert(login_page.is_login_successful(), "Login failed")
                logger.info("Login successful")
            
            with step("Navigate to Edit Address"):
                logger.info("Navigating to addresses")
                profile_page.navigate_to_addresses()
                logger.info("Clicking edit address")
                profile_page.click_edit_address()
            
            with step("Verify address details are displayed correctly"):
                logger.info("Retrieving saved address details")
                address = profile_page.get_address_field_value("billing_address_1")
                city = profile_page.get_address_field_value("billing_city")
                postcode = profile_page.get_address_field_value("billing_postcode")
                logger.info(f"Address: {address}, City: {city}, Postcode: {postcode}")
                log_and_assert("123 Main St" in address, f"Address mismatch: {address}")
                log_and_assert("Chennai" in city, f"City mismatch: {city}")
                log_and_assert("110001" in postcode, f"Postcode mismatch: {postcode}")
                logger.info("Address persistence verified successfully")
        else:
            with step("Login to account"):
                logger.info(f"Starting test: {data['Test Case Title']}")
                if not login_page.is_login_successful():
                    logger.info("Navigating to login page")
                    login_page.navigate_to_login()
                    logger.info("Logging in with credentials")
                    login_page.login("user123@mail.com", "Str0ngPass!")
                    log_and_assert(login_page.is_login_successful(), "Login failed")
                    logger.info("Login successful")

            profile_page = ProfilePage(self.driver)

            with step("Navigate to My Account"):
                logger.info("Navigating to addresses")
                profile_page.navigate_to_addresses()

            with step("Click Edit Address"):
                if "Shipping" in data["Test Case Title"]:
                    logger.info("Clicking edit shipping address")
                    profile_page.click_edit_shipping_address()
                else:
                    logger.info("Clicking edit billing address")
                    profile_page.click_edit_address()

            test_data = str(data.get("Test Data", ""))
            parts = test_data.split()
            street = parts[1] + " " + parts[2] + " " + parts[3] if len(parts) > 3 else "123 Main St"
            city = parts[5] if len(parts) > 5 else "Chennai"
            state = parts[7] if len(parts) > 7 else "Chennai"
            postcode = parts[9] if len(parts) > 9 else "110001"
            country = parts[11] if len(parts) > 11 else "India"

            is_shipping = "Shipping" in data["Test Case Title"]
            with step("Enter valid address details"):
                logger.info(f"Filling address: {street}, {city}, {state}, {postcode}, {country}")
                profile_page.fill_address("Test", "User", "Test Company", "testuser@example.com", 
                                         "9876543210", street, "", city, state, postcode, country, is_shipping)

            with step("Click Save Address"):
                logger.info("Saving address")
                profile_page.save_address()

            with step("Verify address saved successfully"):
                success = profile_page.is_success_message_displayed()
                log_and_assert(success, "Address save failed - success message not displayed")
                logger.info("Address saved successfully")
