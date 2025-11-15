from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input.qty")
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, "button.single_add_to_cart_button")
    VIEW_BASKET_BTN = (By.CSS_SELECTOR, "a.wc-forward, a.button.wc-forward")
    
    def set_quantity(self, quantity):
        element = self.find(*self.QUANTITY_INPUT)
        element.clear()
        element.send_keys(str(quantity))
    
    def click_add_to_basket(self):
        self.click(*self.ADD_TO_BASKET_BTN)
    
    def click_view_basket(self):
        self.click(*self.VIEW_BASKET_BTN)
