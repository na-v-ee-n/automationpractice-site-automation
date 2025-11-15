from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ShopPage(BasePage):
    SHOP_MENU = (By.LINK_TEXT, "Shop")
    PRODUCT_LINK = (By.XPATH, "//h3[text()='{}']")
    ADD_TO_BASKET_BTN = (By.XPATH, "//h3[text()='{}']/following::a[contains(@class,'add_to_cart_button')][1]")
    VIEW_BASKET_BTN = (By.LINK_TEXT, "View Basket")
    
    def navigate_to_shop(self):
        self.click(*self.SHOP_MENU)
    
    def click_product(self, product_name):
        locator = (self.PRODUCT_LINK[0], self.PRODUCT_LINK[1].format(product_name))
        element = self.find(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)
    
    def add_product_to_basket(self, product_name):
        locator = (self.ADD_TO_BASKET_BTN[0], self.ADD_TO_BASKET_BTN[1].format(product_name))
        self.click(*locator)
    
    def click_view_basket(self):
        self.click(*self.VIEW_BASKET_BTN)
