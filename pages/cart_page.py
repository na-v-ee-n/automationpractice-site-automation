from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    PRODUCT_NAME = (By.XPATH, "//td[@class='product-name']/a")
    PRODUCT_PRICE = (By.XPATH, "//td[@class='product-price']/span")
    PRODUCT_QUANTITY = (By.XPATH, "//input[@class='input-text qty text']")
    PRODUCT_SUBTOTAL = (By.XPATH, "//td[@class='product-subtotal']/span")
    REMOVE_BTN = (By.CSS_SELECTOR, "a.remove")
    
    def get_product_name(self):
        return self.get_text(*self.PRODUCT_NAME)
    
    def get_product_price(self):
        return self.get_text(*self.PRODUCT_PRICE)
    
    def get_product_quantity(self):
        return self.find(*self.PRODUCT_QUANTITY).get_attribute("value")
    
    def get_product_subtotal(self):
        return self.get_text(*self.PRODUCT_SUBTOTAL)
    
    def clear_cart(self):
        try:
            while True:
                self.click(*self.REMOVE_BTN)
                self.driver.implicitly_wait(1)
        except:
            pass
