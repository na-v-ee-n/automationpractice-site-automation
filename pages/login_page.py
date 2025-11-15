from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.NAME, "login")
    HELLO_USER = (By.XPATH, "//p[starts-with(normalize-space(),'Hello user')]")
    LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Logout']")
    ERROR_MSG = (By.XPATH, "//strong[text()='Error:']")
    DASHBOARD = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")
    MY_ACCOUNT_BTN = (By.XPATH, "//li/a[text()='My Account']")
    LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Logout']")

    def navigate_to_login(self):
        self.click(self.MY_ACCOUNT_BTN[0], self.MY_ACCOUNT_BTN[1])
        return self.find(self.LOGIN_BTN[0], self.LOGIN_BTN[1]).is_displayed()
    
    def login(self, username, password):
        self.type(self.USERNAME[0], self.USERNAME[1], username)
        self.type(self.PASSWORD[0], self.PASSWORD[1], password)
        self.click(self.LOGIN_BTN[0], self.LOGIN_BTN[1])

    def is_login_successful(self):
        try:
            self.wait.until(lambda driver: driver.find_element(*self.LOGOUT_BTN))
            print("Login Success")
            return True
        except TimeoutException:
            return False
    
    def is_error_displayed(self):
        try:
            error_element = self.wait.until(lambda driver: driver.find_element(*self.ERROR_MSG))
            error_text = error_element.find_element(By.XPATH, "./parent::*").text
            print(f"Login Failed: {error_text}")
            return True
        except TimeoutException:
            return False
    
    def logout(self):
        self.click(self.LOGOUT_BTN[0], self.LOGOUT_BTN[1])
    
    def is_login_button_visible(self):
        try:
            self.wait.until(lambda driver: driver.find_element(*self.LOGIN_BTN))
            print("Logout Success")
            return True
        except TimeoutException:
            return False