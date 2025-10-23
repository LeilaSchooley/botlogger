"""
Selenium Bot for Interacting with Stripe Card Element iFrames
Based on Stack Overflow solution for handling multiple Stripe iframes
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class StripeCardBot:
    """Bot to automate Stripe card payment form interactions"""
    
    def __init__(self, driver=None):
        """
        Initialize the bot with a WebDriver instance
        
        Args:
            driver: Selenium WebDriver instance (if None, creates Chrome driver)
        """
        if driver is None:
            self.driver = webdriver.Chrome()
            self.own_driver = True
        else:
            self.driver = driver
            self.own_driver = False
    
    def wait_for_element(self, by, value, timeout=10):
        """
        Wait for an element to be present and visible
        
        Args:
            by: Selenium By locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None
    
    def find_stripe_iframe_by_name(self, iframe_name):
        """
        Find and switch to a Stripe iframe by name
        
        Args:
            iframe_name: Name of the iframe (e.g., '__privateStripeFrame5')
            
        Returns:
            True if iframe found and switched, False otherwise
        """
        try:
            self.driver.switch_to.default_content()
            iframe = self.wait_for_element(By.NAME, iframe_name)
            if iframe:
                self.driver.switch_to.frame(iframe)
                return True
            return False
        except Exception as e:
            print(f"Error finding iframe {iframe_name}: {e}")
            return False
    
    def find_stripe_iframe_with_element(self, element_name):
        """
        Find the iframe containing a specific element by iterating through all iframes
        
        Args:
            element_name: Name attribute of the element to find
            
        Returns:
            Index of iframe if found, -1 otherwise
        """
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Total iframes found: {len(iframes)}")
        
        for i, iframe in enumerate(iframes):
            try:
                print(f"Checking iframe index: {i}")
                self.driver.switch_to.frame(iframe)
                
                # Try to find the element in current iframe
                elements = self.driver.find_elements(By.NAME, element_name)
                if len(elements) > 0:
                    print(f"Element '{element_name}' found in iframe index: {i}")
                    return i
                else:
                    print(f"Element '{element_name}' NOT found in iframe index: {i}")
                
                self.driver.switch_to.default_content()
            except Exception as e:
                print(f"Error checking iframe {i}: {e}")
                self.driver.switch_to.default_content()
        
        return -1
    
    def enter_card_number(self, card_number, iframe_name="__privateStripeFrame5"):
        """
        Enter credit card number in Stripe iframe
        
        Args:
            card_number: Card number string (e.g., "4242 4242 4242 4242")
            iframe_name: Name of the iframe containing card number field
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering card number: {card_number}")
            
            # Method 1: Try finding iframe by name
            if self.find_stripe_iframe_by_name(iframe_name):
                card_field = self.wait_for_element(By.NAME, "cardnumber")
                if card_field:
                    card_field.click()
                    time.sleep(0.5)
                    card_field.send_keys(card_number)
                    self.driver.switch_to.default_content()
                    print("Card number entered successfully")
                    return True
            
            # Method 2: Search through all iframes
            print("Trying to find card number field by searching all iframes...")
            iframe_index = self.find_stripe_iframe_with_element("cardnumber")
            if iframe_index >= 0:
                card_field = self.driver.find_element(By.NAME, "cardnumber")
                card_field.click()
                time.sleep(0.5)
                card_field.send_keys(card_number)
                self.driver.switch_to.default_content()
                print("Card number entered successfully")
                return True
            
            print("Failed to find card number field")
            return False
            
        except Exception as e:
            print(f"Error entering card number: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def enter_expiry_date(self, exp_date, iframe_name="__privateStripeFrame6"):
        """
        Enter expiry date in Stripe iframe
        
        Args:
            exp_date: Expiry date string (e.g., "1225" for 12/25)
            iframe_name: Name of the iframe containing expiry date field
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering expiry date: {exp_date}")
            
            if self.find_stripe_iframe_by_name(iframe_name):
                exp_field = self.wait_for_element(By.NAME, "exp-date")
                if exp_field:
                    exp_field.click()
                    time.sleep(0.5)
                    exp_field.send_keys(exp_date)
                    self.driver.switch_to.default_content()
                    print("Expiry date entered successfully")
                    return True
            
            print("Failed to find expiry date field")
            return False
            
        except Exception as e:
            print(f"Error entering expiry date: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def enter_cvc(self, cvc, iframe_name="__privateStripeFrame7"):
        """
        Enter CVC/CVV in Stripe iframe
        
        Args:
            cvc: CVC string (e.g., "123")
            iframe_name: Name of the iframe containing CVC field
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering CVC: {cvc}")
            
            if self.find_stripe_iframe_by_name(iframe_name):
                cvc_field = self.wait_for_element(By.NAME, "cvc")
                if cvc_field:
                    cvc_field.click()
                    time.sleep(0.5)
                    cvc_field.send_keys(cvc)
                    self.driver.switch_to.default_content()
                    print("CVC entered successfully")
                    return True
            
            print("Failed to find CVC field")
            return False
            
        except Exception as e:
            print(f"Error entering CVC: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def enter_zip_code(self, zip_code, iframe_name="__privateStripeFrame8"):
        """
        Enter ZIP/Postal code in Stripe iframe (if present)
        
        Args:
            zip_code: ZIP code string
            iframe_name: Name of the iframe containing postal code field
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering ZIP code: {zip_code}")
            
            if self.find_stripe_iframe_by_name(iframe_name):
                zip_field = self.wait_for_element(By.NAME, "postal")
                if zip_field:
                    zip_field.click()
                    time.sleep(0.5)
                    zip_field.send_keys(zip_code)
                    self.driver.switch_to.default_content()
                    print("ZIP code entered successfully")
                    return True
            
            print("ZIP code field not found (may not be required)")
            return False
            
        except Exception as e:
            print(f"Error entering ZIP code: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def enter_cardholder_name(self, name):
        """
        Enter cardholder name (usually not in iframe)
        
        Args:
            name: Cardholder name string
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering cardholder name: {name}")
            self.driver.switch_to.default_content()
            
            # Try common field names
            field_names = ["name_on_card", "cardholder-name", "card-name", "name"]
            
            for field_name in field_names:
                try:
                    name_field = self.driver.find_element(By.NAME, field_name)
                    if name_field:
                        name_field.click()
                        time.sleep(0.5)
                        name_field.send_keys(name)
                        print("Cardholder name entered successfully")
                        return True
                except NoSuchElementException:
                    continue
            
            print("Cardholder name field not found")
            return False
            
        except Exception as e:
            print(f"Error entering cardholder name: {e}")
            return False
    
    def fill_card_details(self, card_number, exp_date, cvc, name=None, zip_code=None):
        """
        Fill all card details in Stripe payment form
        
        Args:
            card_number: Card number (e.g., "4242 4242 4242 4242")
            exp_date: Expiry date (e.g., "1225" for 12/25)
            cvc: CVC code (e.g., "123")
            name: Optional cardholder name
            zip_code: Optional ZIP/postal code
            
        Returns:
            True if all fields filled successfully, False otherwise
        """
        print("=" * 60)
        print("Starting to fill Stripe card details...")
        print("=" * 60)
        
        success = True
        
        # Wait for page to load
        time.sleep(2)
        
        # Fill card number
        if not self.enter_card_number(card_number):
            success = False
        
        # Fill expiry date
        if not self.enter_expiry_date(exp_date):
            success = False
        
        # Fill CVC
        if not self.enter_cvc(cvc):
            success = False
        
        # Fill ZIP code if provided
        if zip_code:
            self.enter_zip_code(zip_code)
        
        # Fill cardholder name if provided
        if name:
            self.enter_cardholder_name(name)
        
        print("=" * 60)
        if success:
            print("All required card details filled successfully!")
        else:
            print("Some fields failed to fill. Please check the logs.")
        print("=" * 60)
        
        return success
    
    def submit_form(self):
        """
        Submit the payment form
        
        Returns:
            True if submit button clicked, False otherwise
        """
        try:
            self.driver.switch_to.default_content()
            
            # Try common submit button selectors
            selectors = [
                (By.TAG_NAME, "button[type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[@type='submit']"),
                (By.TAG_NAME, "button"),
            ]
            
            for by, selector in selectors:
                try:
                    button = self.driver.find_element(by, selector)
                    if button:
                        button.click()
                        print("Submit button clicked")
                        return True
                except NoSuchElementException:
                    continue
            
            print("Submit button not found")
            return False
            
        except Exception as e:
            print(f"Error submitting form: {e}")
            return False
    
    def close(self):
        """Close the WebDriver if it was created by this bot"""
        if self.own_driver and self.driver:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Test card numbers for Stripe (these won't charge real money)
    TEST_CARD_SUCCESS = "4242 4242 4242 4242"
    TEST_CARD_DECLINE = "4000 0000 0000 0002"
    
    # Create bot instance
    bot = StripeCardBot()
    
    try:
        # Navigate to your payment page
        # bot.driver.get("https://your-payment-page-url.com")
        
        # Fill card details
        bot.fill_card_details(
            card_number=TEST_CARD_SUCCESS,
            exp_date="1225",  # December 2025
            cvc="123",
            name="Test User",
            zip_code="12345"
        )
        
        # Optional: Submit the form
        # bot.submit_form()
        
        # Keep browser open for inspection
        input("Press Enter to close the browser...")
        
    finally:
        bot.close()
