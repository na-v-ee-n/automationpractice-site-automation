from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidElementStateException
from pages.base_page import BasePage

class ProfilePage(BasePage):
    ADDRESSES_LINK = (By.XPATH, "//a[contains(text(),'Addresses')]")
    EDIT_ADDRESS_BTN = (By.XPATH, "//a[contains(@href,'edit-address/billing')]")
    EDIT_SHIPPING_BTN = (By.XPATH, "//a[contains(@href,'edit-address/shipping')]")
    FIRST_NAME = (By.ID, "billing_first_name")
    LAST_NAME = (By.ID, "billing_last_name")
    COMPANY = (By.ID, "billing_company")
    EMAIL = (By.ID, "billing_email")
    PHONE = (By.ID, "billing_phone")
    ADDRESS_1 = (By.ID, "billing_address_1")
    ADDRESS_2 = (By.ID, "billing_address_2")
    CITY = (By.ID, "billing_city")
    STATE = (By.ID, "billing_state")
    POSTCODE = (By.ID, "billing_postcode")
    COUNTRY = (By.ID, "billing_country")
    SHIPPING_FIRST_NAME = (By.ID, "shipping_first_name")
    SHIPPING_LAST_NAME = (By.ID, "shipping_last_name")
    SHIPPING_COMPANY = (By.ID, "shipping_company")
    SHIPPING_ADDRESS_1 = (By.ID, "shipping_address_1")
    SHIPPING_ADDRESS_2 = (By.ID, "shipping_address_2")
    SHIPPING_CITY = (By.ID, "shipping_city")
    SHIPPING_STATE = (By.ID, "shipping_state")
    SHIPPING_POSTCODE = (By.ID, "shipping_postcode")
    SHIPPING_COUNTRY = (By.ID, "shipping_country")
    SAVE_ADDRESS_BTN = (By.NAME, "save_address")
    SUCCESS_MSG = (By.XPATH, "//div[contains(@class,'woocommerce-message')]")

    def navigate_to_addresses(self):
        self.click(*self.ADDRESSES_LINK)

    def click_edit_address(self):
        self.click(*self.EDIT_ADDRESS_BTN)

    def click_edit_shipping_address(self):
        self.click(*self.EDIT_SHIPPING_BTN)

    def fill_address(self, first_name, last_name, company, email, phone, street, address_2, city, state, postcode, country, is_shipping=False):
        if is_shipping:
            self.type(*self.SHIPPING_FIRST_NAME, first_name)
            self.type(*self.SHIPPING_LAST_NAME, last_name)
            self.type(*self.SHIPPING_COMPANY, company)
            self.type(*self.SHIPPING_ADDRESS_1, street)
            self.type(*self.SHIPPING_ADDRESS_2, address_2)
            self.type(*self.SHIPPING_CITY, city)
            try:
                self.type(*self.SHIPPING_STATE, state)
            except InvalidElementStateException:
                pass
            self.type(*self.SHIPPING_POSTCODE, postcode)
            Select(self.find(*self.SHIPPING_COUNTRY)).select_by_visible_text(country)
        else:
            self.type(*self.FIRST_NAME, first_name)
            self.type(*self.LAST_NAME, last_name)
            self.type(*self.COMPANY, company)
            self.type(*self.EMAIL, email)
            self.type(*self.PHONE, phone)
            self.type(*self.ADDRESS_1, street)
            self.type(*self.ADDRESS_2, address_2)
            self.type(*self.CITY, city)
            try:
                self.type(*self.STATE, state)
            except InvalidElementStateException:
                pass
            self.type(*self.POSTCODE, postcode)
            Select(self.find(*self.COUNTRY)).select_by_visible_text(country)

    def save_address(self):
        self.click(*self.SAVE_ADDRESS_BTN)

    def is_success_message_displayed(self):
        return "Address changed successfully" in self.get_text(*self.SUCCESS_MSG)

    def get_address_field_value(self, field_id):
        return self.find(By.ID, field_id).get_attribute("value")
