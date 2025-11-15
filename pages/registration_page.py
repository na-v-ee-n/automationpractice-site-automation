from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    EMAIL = (By.ID, "reg_email")
    PASSWORD = (By.ID, "reg_password")
    REGISTER_BTN = (By.NAME, "register")
    ERROR_MSG = (By.CSS_SELECTOR, ".woocommerce-error li")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")
    PASSWORD_STRENGTH_TEXT = (By.XPATH, "//div[@class='woocommerce-password-strength bad']")
    HELLO_USER = (By.XPATH, "//p[starts-with(normalize-space(),'Hello user')]")
    LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Logout']")
    
    def register(self, email, password):
        self.type(*self.EMAIL, email)
        self.type(*self.PASSWORD, password)
        self.click(*self.REGISTER_BTN)

    def get_error_message(self):
        return self.get_text(*self.ERROR_MSG)

    def is_registration_successful(self):
        return self.find(*self.SUCCESS_MSG)
