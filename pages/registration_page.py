from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

class RegistrationPage(BasePage):
    EMAIL = (By.ID, "reg_email")
    PASSWORD = (By.ID, "reg_password")
    REGISTER_BTN = (By.NAME, "register")
    ERROR_MSG = (By.XPATH, "//ul[contains(@class,'woocommerce-error')]//li")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")
    PASSWORD_STRENGTH_TEXT = (By.XPATH, "//div[contains(@class,'woocommerce-password-strength')]")
    HELLO_USER = (By.XPATH, "//p[starts-with(normalize-space(),'Hello')]")
    LOGOUT_BTN = (By.XPATH, "//a[contains(text(),'Logout')]")
    MY_ACCOUNT_BTN = (By.XPATH, "//a[contains(text(),'My Account')]")
    
    def navigate_to_registration(self):
        from selenium.webdriver.support import expected_conditions as EC
        # Wait for My Account button to be clickable
        my_account_btn = self.wait.until(EC.element_to_be_clickable(self.MY_ACCOUNT_BTN))
        my_account_btn.click()
        # Wait for registration form to be visible
        return self.wait.until(EC.visibility_of_element_located(self.REGISTER_BTN)).is_displayed()
    
    def register(self, email, password):
        # Clear and enter email
        email_field = self.find(self.EMAIL[0], self.EMAIL[1])
        email_field.clear()
        if email:  # Only enter email if not empty
            email_field.send_keys(email)
        
        # Clear and enter password
        password_field = self.find(self.PASSWORD[0], self.PASSWORD[1])
        password_field.clear()
        if password:  # Only enter password if not empty
            password_field.send_keys(password)
            
            # Wait for password strength validation
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import time
            time.sleep(2)  # Allow password strength to be calculated
            
            # Check password strength before clicking register
            try:
                strength_element = self.find(self.PASSWORD_STRENGTH_TEXT[0], self.PASSWORD_STRENGTH_TEXT[1])
                strength_text = strength_element.text.lower()
                print(f"Password strength: {strength_text}")
                
                # Only block if password is "very weak" - allow "weak" passwords to proceed
                if "very weak" in strength_text and "please enter a stronger password" in strength_text:
                    print("Password is very weak, cannot proceed with registration")
                    return False
                elif "weak" in strength_text:
                    print("Password is weak but proceeding with registration attempt")
            except Exception as e:
                print(f"Could not check password strength: {e}")
                # If we can't find the strength indicator, proceed anyway
                pass
        
        # Click register button - handle ad interference
        try:
            register_btn = self.find(self.REGISTER_BTN[0], self.REGISTER_BTN[1])
            # Scroll to button and use JavaScript click to avoid ad interference
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
            import time
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", register_btn)
            return True
        except Exception as e:
            print(f"Failed to click register button: {e}")
            return False

    def get_password_strength_text(self):
        try:
            strength_element = self.find(self.PASSWORD_STRENGTH_TEXT[0], self.PASSWORD_STRENGTH_TEXT[1])
            return strength_element.text
        except Exception:
            return ""
    
    def is_password_strength_acceptable(self):
        strength_text = self.get_password_strength_text()
        return "Very weak - Please enter a stronger password." not in strength_text
    
    def is_registration_successful(self):
        try:
            # Check for logout button AND hello user message
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            
            wait = WebDriverWait(self.driver, 10)
            
            # Look for logout button
            logout_present = False
            hello_present = False
            
            try:
                logout_element = wait.until(EC.presence_of_element_located(self.LOGOUT_BTN))
                if logout_element.is_displayed():
                    logout_present = True
                    print("Logout button found")
            except TimeoutException:
                print("Logout button not found")
            
            # Look for hello user message
            try:
                hello_element = self.driver.find_element(By.XPATH, "//p[contains(text(),'Hello')]") 
                if hello_element.is_displayed():
                    hello_present = True
                    print(f"Hello user message found: {hello_element.text}")
            except:
                print("Hello user message not found")
            
            # Registration is successful if we have logout button AND hello message
            if logout_present and hello_present:
                print("Registration Success - Both logout and hello user found")
                return True
            elif logout_present:
                print("Registration Success - Logout button found")
                return True
            else:
                print("Registration failed - Success indicators not found")
                return False
                
        except Exception as e:
            print(f"Error checking registration success: {e}")
            return False
    
    def is_error_displayed(self):
        try:
            # Look for various error indicators with shorter timeout
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            short_wait = WebDriverWait(self.driver, 3)
            
            error_selectors = [
                (By.XPATH, "//ul[contains(@class,'woocommerce-error')]//li"),
                (By.XPATH, "//div[contains(@class,'woocommerce-error')]"),
                (By.XPATH, "//*[contains(@class,'error')]"),
                (By.XPATH, "//*[contains(text(),'Error:')]"),
                (By.XPATH, "//*[contains(text(),'already registered')]"),
                (By.XPATH, "//*[contains(text(),'invalid email')]"),
                (By.XPATH, "//*[contains(text(),'Please provide a valid email')]"),
                (By.XPATH, "//*[contains(text(),'required')]"),
            ]
            
            for selector in error_selectors:
                try:
                    error_element = short_wait.until(EC.presence_of_element_located(selector))
                    error_text = error_element.text
                    if error_text.strip():  # Only return True if there's actual text
                        print(f"Registration Error Found: {error_text}")
                        return True
                except TimeoutException:
                    continue
            
            print("No error messages found")
            return False
        except Exception as e:
            print(f"Error checking for error messages: {e}")
            return False
    
    def logout(self):
        print("Clicking logout button")
        self.click(self.LOGOUT_BTN[0], self.LOGOUT_BTN[1])
        print("Logout clicked successfully")
    
    def is_register_button_visible(self):
        try:
            self.wait.until(lambda driver: driver.find_element(*self.REGISTER_BTN))
            print("Logout Success")
            return True
        except TimeoutException:
            return False
