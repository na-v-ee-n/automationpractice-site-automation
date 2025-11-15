import pytest
import allure
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.excel_reader import read_test_data
from utils.test_helper import step, attach_text, log_and_assert
from testdata.data_paths import CART_TESTCASES

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("setup")
class TestCart:

    @allure.title("Cart Test - {data[Test Case Title]}")
    @allure.description("Test cart functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("data", read_test_data(CART_TESTCASES, "Sheet1"))
    def test_add_to_cart(self, data):
        module = data["Module"]
        logger.info(f"Starting test: {data['Test Case Title']}")
        
        if module == "Delete from Cart":
            self._test_delete_from_cart(data)
        elif module == "Add to Cart":
            result = self._test_add_to_cart(data)
            if result == "clear_cart":
                logger.info("Cleaning up cart after test")
                try:
                    self.driver.get("https://practice.automationtesting.in/basket")
                    time.sleep(2)
                    remove_btns = self.driver.find_elements(By.CSS_SELECTOR, "a.remove")
                    for btn in remove_btns:
                        try:
                            self.driver.execute_script("arguments[0].click();", btn)
                            time.sleep(1)
                        except:
                            pass
                except:
                    pass
        else:
            pytest.skip("Unknown module")
        
        logger.info(f"Test completed: {data['Test Case Title']}")
    
    def _test_delete_from_cart(self, data):
        shop_page = ShopPage(self.driver)
        wait = WebDriverWait(self.driver, 10)
        preconditions = data.get("Preconditions", "")
        
        with step("Clear existing cart"):
            logger.info("Clearing existing cart items")
            try:
                self.driver.get("https://practice.automationtesting.in/basket")
                time.sleep(2)
                remove_btns = self.driver.find_elements(By.CSS_SELECTOR, "a.remove")
                logger.info(f"Found {len(remove_btns)} items to remove")
                for btn in remove_btns:
                    try:
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
                    except:
                        pass
            except:
                pass
        
        if "Basket contains" in preconditions:
            products = preconditions.replace("Basket contains ", "").split(" and ")
            logger.info(f"Setting up precondition: Adding {products}")
            
            with step(f"Add products to basket: {', '.join(products)}"):
                shop_page.navigate_to_shop()
                for product in products:
                    logger.info(f"Adding product: {product.strip()}")
                    shop_page.add_product_to_basket(product.strip())
                    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "View Basket")))
                    time.sleep(1)
        
        with step("Navigate to Basket page"):
            logger.info("Navigating to basket page")
            self.driver.get("https://practice.automationtesting.in/basket")
            time.sleep(2)
        
        if len(products) > 1:
            product_to_remove = products[1].strip()
            logger.info(f"Removing product: {product_to_remove}")
            
            with step(f"Remove {product_to_remove} from basket"):
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.cart_item")
                for row in rows:
                    product_name = row.find_element(By.CSS_SELECTOR, "td.product-name a").text
                    if product_to_remove in product_name:
                        logger.info(f"Found product to remove: {product_name}")
                        remove_btn = row.find_element(By.CSS_SELECTOR, "a.remove")
                        self.driver.execute_script("arguments[0].click();", remove_btn)
                        time.sleep(3)
                        break
            
            with step("Verify remaining product and total"):
                remaining_product = self.driver.find_element(By.XPATH, "//td[@class='product-name']/a").text
                logger.info(f"Remaining product: {remaining_product}")
                attach_text(remaining_product, "Remaining Product")
                log_and_assert(products[0].strip() in remaining_product, f"Expected {products[0]} to remain")
                
                if "total" in data["Expected Result"].lower():
                    total_elem = self.driver.find_element(By.XPATH, "//tr[@class='order-total']//span[@class='woocommerce-Price-amount amount']")
                    actual_total = total_elem.text
                    expected_total = data["Expected Result"].split("total ")[1]
                    logger.info(f"Expected total: {expected_total}, Actual total: {actual_total}")
                    actual_total_clean = actual_total.replace(",", "")
                    expected_total_clean = expected_total.replace(",", "")
                    log_and_assert(expected_total_clean in actual_total_clean, f"Expected total '{expected_total}' but got '{actual_total}'")
        else:
            with step("Remove product from basket"):
                logger.info("Removing single product from basket")
                remove_btn = self.driver.find_element(By.CSS_SELECTOR, "a.remove")
                self.driver.execute_script("arguments[0].click();", remove_btn)
                time.sleep(3)
            
            with step("Verify basket is empty"):
                cart_items = self.driver.find_elements(By.CSS_SELECTOR, "tr.cart_item")
                logger.info(f"Cart items count after removal: {len(cart_items)}")
                log_and_assert(len(cart_items) == 0, f"Expected 0 items in cart but found {len(cart_items)}")
    
    def _test_add_to_cart(self, data):
        test_data = str(data.get("Test Data", ""))
        shop_page = ShopPage(self.driver)
        cart_page = CartPage(self.driver)
        wait = WebDriverWait(self.driver, 10)
        
        if "Basket empty" in data.get("Preconditions", ""):
            with step("Clear cart"):
                logger.info("Clearing cart as per precondition")
                try:
                    self.driver.get("https://practice.automationtesting.in/basket")
                    time.sleep(2)
                    remove_btns = self.driver.find_elements(By.CSS_SELECTOR, "a.remove")
                    logger.info(f"Found {len(remove_btns)} items to clear")
                    for btn in remove_btns:
                        try:
                            self.driver.execute_script("arguments[0].click();", btn)
                            time.sleep(1)
                        except:
                            pass
                except:
                    pass
        
        with step("Navigate to Shop page"):
            logger.info("Navigating to shop page")
            shop_page.navigate_to_shop()

        if "Product1:" in test_data:
            product1 = test_data.split("Product1: ")[1].split(" ₹")[0]
            product2 = test_data.split("Product2: ")[1].split(" ₹")[0]
            logger.info(f"Adding multiple products: {product1}, {product2}")
            
            with step(f"Add product '{product1}' to basket"):
                shop_page.add_product_to_basket(product1)
                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "View Basket")))
                logger.info(f"Product 1 added: {product1}")
                attach_text(product1, "Product 1 Added")
            
            with step(f"Add product '{product2}' to basket"):
                shop_page.add_product_to_basket(product2)
                time.sleep(2)
                logger.info(f"Product 2 added: {product2}")
                attach_text(product2, "Product 2 Added")
            
            with step("Click View Basket"):
                shop_page.click_view_basket()
            
            with step("Verify multiple products in cart"):
                products = self.driver.find_elements(By.XPATH, "//td[@class='product-name']/a")
                product_names = [p.text for p in products]
                logger.info(f"Products in cart: {product_names}")
                
                attach_text(f"Products in cart: {', '.join(product_names)}", "Cart Products")
                
                log_and_assert(product1 in product_names, f"Product '{product1}' not found in cart")
                log_and_assert(product2 in product_names, f"Product '{product2}' not found in cart")
                
                if "total" in data["Expected Result"].lower():
                    total_elem = self.driver.find_element(By.XPATH, "//tr[@class='order-total']//span[@class='woocommerce-Price-amount amount']")
                    actual_total = total_elem.text
                    expected_total = data["Expected Result"].split("total ")[1]
                    logger.info(f"Expected total: {expected_total}, Actual total: {actual_total}")
                    actual_total_clean = actual_total.replace(",", "")
                    expected_total_clean = expected_total.replace(",", "")
                    log_and_assert(expected_total_clean in actual_total_clean, f"Expected total '{expected_total}' but got '{actual_total}'")
            
            return "clear_cart"
        else:
            product_name = test_data.split("Product: ")[1].split(",")[0] if "Product:" in test_data else "Selenium Ruby"
            quantity = int(test_data.split("Quantity: ")[1]) if "Quantity:" in test_data else 1
            expected_price = test_data.split("Price: ")[1] if "Price:" in test_data else "₹500.00"
            logger.info(f"Adding product: {product_name}, Quantity: {quantity}")

            if quantity > 1:
                with step(f"Click product '{product_name}'"):
                    shop_page.click_product(product_name)
                    logger.info(f"Clicked on product: {product_name}")
                
                with step(f"Set quantity to {quantity} and add to basket"):
                    product_page = ProductPage(self.driver)
                    product_page.set_quantity(quantity)
                    logger.info(f"Set quantity to: {quantity}")
                    product_page.click_add_to_basket()
                    attach_text(f"{product_name} x {quantity}", "Product Added")
                
                with step("Click View Basket"):
                    product_page.click_view_basket()
            else:
                with step(f"Add product '{product_name}' to basket"):
                    shop_page.add_product_to_basket(product_name)
                    logger.info(f"Product added: {product_name}")
                    attach_text(product_name, "Product Added")
                
                with step("Click View Basket"):
                    shop_page.click_view_basket()

            with step("Verify product in cart"):
                actual_product = cart_page.get_product_name()
                actual_price = cart_page.get_product_price()
                actual_quantity = cart_page.get_product_quantity()
                actual_subtotal = cart_page.get_product_subtotal()
                
                logger.info(f"Cart verification - Product: {actual_product}, Price: {actual_price}, Quantity: {actual_quantity}, Subtotal: {actual_subtotal}")

                attach_text(f"Product: {actual_product}\nPrice: {actual_price}\nQuantity: {actual_quantity}\nSubtotal: {actual_subtotal}", "Cart Details")

                log_and_assert(product_name in actual_product, f"Expected product '{product_name}' not found in cart")
                log_and_assert(actual_quantity == str(quantity), f"Expected quantity {quantity} but got '{actual_quantity}'")
                
                if "Expected Result" in data:
                    expected_result = data["Expected Result"]
                    if "subtotal" in expected_result.lower():
                        expected_subtotal = expected_result.split("subtotal ")[1].split(",")[0] if "subtotal" in expected_result else expected_price
                        actual_subtotal_clean = actual_subtotal.replace(",", "")
                        expected_subtotal_clean = expected_subtotal.replace(",", "")
                        logger.info(f"Expected subtotal: {expected_subtotal}, Actual subtotal: {actual_subtotal}")
                        log_and_assert(expected_subtotal_clean in actual_subtotal_clean, f"Expected subtotal '{expected_subtotal}' but got '{actual_subtotal}'")
                    else:
                        log_and_assert(expected_price in actual_subtotal, f"Expected subtotal '{expected_price}' but got '{actual_subtotal}'")
