"""
Selenium Bot for Lemon Squeezy Payment Forms
Handles Stripe payment elements embedded in Lemon Squeezy checkout pages
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
import time


class LemonSqueezyBot:
    """Bot to automate Lemon Squeezy payment form interactions"""
    
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
        """Wait for an element to be present and visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None
    
    def wait_for_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for clickable element: {value}")
            return None
    
    def find_stripe_iframe_by_name_pattern(self, pattern):
        """
        Find Stripe iframe by name pattern
        
        Args:
            pattern: Part of the iframe name to match
            
        Returns:
            True if found and switched, False otherwise
        """
        try:
            self.driver.switch_to.default_content()
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                name = iframe.get_attribute("name")
                if name and pattern in name:
                    print(f"Found iframe: {name}")
                    self.driver.switch_to.frame(iframe)
                    return True
            
            return False
        except Exception as e:
            print(f"Error finding iframe with pattern {pattern}: {e}")
            return False
    
    def find_stripe_iframe_with_element(self, element_name):
        """
        Find the iframe containing a specific element by iterating through all iframes
        
        Args:
            element_name: Name attribute of the element to find
            
        Returns:
            True if found, False otherwise
        """
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Total iframes found: {len(iframes)}")
        
        for i, iframe in enumerate(iframes):
            try:
                self.driver.switch_to.frame(iframe)
                
                # Try to find the element in current iframe
                elements = self.driver.find_elements(By.NAME, element_name)
                if len(elements) > 0:
                    print(f"Element '{element_name}' found in iframe index: {i}")
                    return True
                
                self.driver.switch_to.default_content()
            except Exception as e:
                print(f"Error checking iframe {i}: {e}")
                self.driver.switch_to.default_content()
        
        return False
    
    def enter_email(self, email):
        """
        Enter email address in Lemon Squeezy form
        
        Args:
            email: Email address
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering email: {email}")
            self.driver.switch_to.default_content()
            time.sleep(1)
            
            # Find the email iframe (link-authentication-element)
            if self.find_stripe_iframe_by_name_pattern("__privateStripeFrame"):
                time.sleep(1)
                # Try to find email field
                try:
                    email_field = self.wait_for_element(By.NAME, "email", timeout=5)
                    if email_field:
                        email_field.click()
                        time.sleep(0.5)
                        email_field.send_keys(email)
                        self.driver.switch_to.default_content()
                        print("Email entered successfully")
                        return True
                except:
                    pass
            
            self.driver.switch_to.default_content()
            print("Email field not found or not required")
            return False
            
        except Exception as e:
            print(f"Error entering email: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def click_send_code_to_email(self):
        """
        Click the "Send code to email instead" button if OTP prompt appears
        
        Returns:
            True if button clicked, False otherwise
        """
        try:
            print("Looking for 'Send code to email instead' button...")
            self.driver.switch_to.default_content()
            time.sleep(1)
            
            # Try to find the button by text content
            try:
                button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Send code to email instead')]", timeout=3)
                if button:
                    print("Found 'Send code to email instead' button")
                    button.click()
                    print("Clicked button - waiting for email code option")
                    time.sleep(2)
                    return True
            except:
                pass
            
            # Try by class
            try:
                button = self.wait_for_element(By.CSS_SELECTOR, ".p-LinkEmailOTP-action", timeout=3)
                if button:
                    print("Found email OTP button by class")
                    button.click()
                    print("Clicked button")
                    time.sleep(2)
                    return True
            except:
                pass
            
            print("'Send code to email' button not found")
            return False
            
        except Exception as e:
            print(f"Error clicking send code button: {e}")
            return False
    
    def enter_link_otp_code(self, code="000000"):
        """
        Enter the Stripe Link OTP code (appears after email entry in test mode)
        
        Args:
            code: OTP code (default "000000" for test mode)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering Link OTP code: {code}")
            self.driver.switch_to.default_content()
            time.sleep(2)  # Wait for OTP prompt to appear
            
            # Find the OTP input field by test ID or other selectors
            try:
                # Try by data-testid
                otp_field = self.wait_for_element(By.CSS_SELECTOR, "[data-testid='code-controlling-input']", timeout=5)
                if otp_field:
                    print("Found OTP input field by data-testid")
                    otp_field.click()
                    time.sleep(0.5)
                    otp_field.send_keys(code)
                    print("OTP code entered successfully")
                    time.sleep(2)  # Wait for code to be processed
                    return True
            except:
                pass
            
            # Try by name attribute
            try:
                otp_field = self.wait_for_element(By.NAME, "codeControllingInput", timeout=5)
                if otp_field:
                    print("Found OTP input field by name")
                    otp_field.click()
                    time.sleep(0.5)
                    otp_field.send_keys(code)
                    print("OTP code entered successfully")
                    time.sleep(2)
                    return True
            except:
                pass
            
            # Try by class name
            try:
                otp_field = self.wait_for_element(By.CLASS_NAME, "p-CodePuncher-controllingInput", timeout=5)
                if otp_field:
                    print("Found OTP input field by class")
                    otp_field.click()
                    time.sleep(0.5)
                    otp_field.send_keys(code)
                    print("OTP code entered successfully")
                    time.sleep(2)
                    return True
            except:
                pass
            
            # Try by input type and autocomplete attribute
            try:
                otp_field = self.wait_for_element(By.CSS_SELECTOR, "input[autocomplete='one-time-code']", timeout=5)
                if otp_field:
                    print("Found OTP input field by autocomplete attribute")
                    otp_field.click()
                    time.sleep(0.5)
                    otp_field.send_keys(code)
                    print("OTP code entered successfully")
                    time.sleep(2)
                    return True
            except:
                pass
            
            print("OTP field not found - may not be required")
            return False
            
        except Exception as e:
            print(f"Error entering OTP code: {e}")
            return False
    
    def enter_card_details_in_payment_element(self, card_number, exp_date, cvc):
        """
        Enter card details in Stripe Payment Element iframe
        
        Args:
            card_number: Card number
            exp_date: Expiry date (MMYY format)
            cvc: CVC code
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print("Entering card details in payment element...")
            self.driver.switch_to.default_content()
           # time.sleep(2)
            
            # Find the payment element iframe
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for i, iframe in enumerate(iframes):
                try:
                    title = iframe.get_attribute("title")
                    name = iframe.get_attribute("name")
                    
                    # Look for payment input frame
                    if title and "payment input" in title.lower():
                        print(f"Found payment iframe at index {i}: {title}")
                        self.driver.switch_to.frame(iframe)
                        time.sleep(1)
                        
                        # Enter card number
                        try:
                            card_field = self.wait_for_element(By.NAME, "number", timeout=5)
                            if not card_field:
                                card_field = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='Card number']", timeout=5)
                            
                            if card_field:
                                print("Entering card number...")
                                card_field.click()
                                #time.sleep(0.5)
                                card_field.send_keys(card_number)
                                #time.sleep(0.5)
                        except Exception as e:
                            print(f"Error entering card number: {e}")
                        
                        # Enter expiry date
                        try:
                            exp_field = self.wait_for_element(By.NAME, "expiry", timeout=5)
                            if not exp_field:
                                exp_field = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='MM']", timeout=5)
                            
                            if exp_field:
                                print("Entering expiry date...")
                                exp_field.click()
                                #time.sleep(0.5)
                                exp_field.send_keys(exp_date)
                                #time.sleep(0.5)
                        except Exception as e:
                            print(f"Error entering expiry date: {e}")
                        
                        # Enter CVC
                        try:
                            cvc_field = self.wait_for_element(By.NAME, "cvc", timeout=5)
                            if not cvc_field:
                                cvc_field = self.wait_for_element(By.CSS_SELECTOR, "input[placeholder*='CVC']", timeout=5)
                            
                            if cvc_field:
                                print("Entering CVC...")
                                cvc_field.click()
                                #time.sleep(0.5)
                                cvc_field.send_keys(cvc)
                                #time.sleep(0.5)
                        except Exception as e:
                            print(f"Error entering CVC: {e}")
                        
                        self.driver.switch_to.default_content()
                        print("Card details entered successfully")
                        return True
                        
                except Exception as e:
                    print(f"Error processing iframe {i}: {e}")
                    self.driver.switch_to.default_content()
            
            print("Payment element iframe not found")
            return False
            
        except Exception as e:
            print(f"Error entering card details: {e}")
            self.driver.switch_to.default_content()
            return False
    
    def enter_cardholder_name(self, name):
        """
        Enter cardholder name (outside iframe)
        
        Args:
            name: Cardholder name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Entering cardholder name: {name}")
            self.driver.switch_to.default_content()
            #time.sleep(0.5)
            
            # Try to find name field by ID
            try:
                name_field = self.driver.find_element(By.ID, "name")
                name_field.click()
                #time.sleep(0.5)
                name_field.clear()
                name_field.send_keys(name)
                print("Cardholder name entered successfully")
                return True
            except NoSuchElementException:
                pass
            
            # Try by dusk attribute
            try:
                name_field = self.driver.find_element(By.CSS_SELECTOR, "[dusk='checkout-form-name']")
                name_field.click()
                #time.sleep(0.5)
                name_field.clear()
                name_field.send_keys(name)
                print("Cardholder name entered successfully")
                return True
            except NoSuchElementException:
                pass
            
            print("Cardholder name field not found")
            return False
            
        except Exception as e:
            print(f"Error entering cardholder name: {e}")
            return False
    
    def select_country(self, country_code="US"):
        """
        Select billing country
        
        Args:
            country_code: Two-letter country code (e.g., "US", "GB", "CA")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Selecting country: {country_code}")
            self.driver.switch_to.default_content()
            
            country_select = Select(self.driver.find_element(By.ID, "country"))
            country_select.select_by_value(country_code)
            print("Country selected successfully")
            return True
            
        except Exception as e:
            print(f"Error selecting country: {e}")
            return False
    
    def enter_billing_address(self, address_line1, city, postal_code, state=None):
        """
        Enter billing address details
        
        Args:
            address_line1: Street address
            city: City name
            postal_code: ZIP/Postal code
            state: State/Province (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print("Entering billing address...")
            self.driver.switch_to.default_content()
            
            # Address line 1
            try:
                addr_field = self.driver.find_element(By.CSS_SELECTOR, "[dusk='checkout-form-line1']")
                addr_field.click()
                #time.sleep(0.5)
                addr_field.send_keys(address_line1)
                print(f"Address: {address_line1}")
            except Exception as e:
                print(f"Could not enter address line 1: {e}")
            
            # City
            try:
                city_field = self.driver.find_element(By.ID, "city")
                city_field.click()
                #time.sleep(0.5)
                city_field.send_keys(city)
                print(f"City: {city}")
            except Exception as e:
                print(f"Could not enter city: {e}")
            
            # Postal code
            try:
                postal_field = self.driver.find_element(By.ID, "postal_code")
                postal_field.click()
                #time.sleep(0.5)
                postal_field.send_keys(postal_code)
                print(f"Postal code: {postal_code}")
            except Exception as e:
                print(f"Could not enter postal code: {e}")
            
            # State (if provided)
            if state:
                try:
                    # Try as a v-select dropdown first (common in Lemon Squeezy)
                    state_input = self.driver.find_element(By.CSS_SELECTOR, "#state input.vs__search")
                    state_input.click()
                    #time.sleep(0.5)
                    state_input.send_keys(state)
                    time.sleep(0.5)
                    # Press Enter to select the first match
                    state_input.send_keys("\n")
                    print(f"State: {state}")
                except:
                    try:
                        # Try as regular input field
                        state_field = self.driver.find_element(By.ID, "state")
                        state_field.click()
                        time.sleep(0.5)
                        state_field.clear()
                        state_field.send_keys(state)
                        print(f"State: {state}")
                    except Exception as e:
                        print(f"Could not enter state: {e}")
            
            print("Billing address entered successfully")
            return True
            
        except Exception as e:
            print(f"Error entering billing address: {e}")
            return False
    
    def fill_complete_form(self, email, card_number, exp_date, cvc, name, 
                          country="US", address="123 Main St", city="New York", 
                          postal_code="10001", state="New York", otp_code="000000"):
        """
        Fill the complete Lemon Squeezy payment form
        
        Args:
            email: Email address
            card_number: Card number
            exp_date: Expiry date (MMYY)
            cvc: CVC code
            name: Cardholder name
            country: Country code (default "US")
            address: Street address
            city: City name
            postal_code: ZIP/Postal code
            state: State/Province (default "New York" for US addresses)
            otp_code: OTP code for Link authentication (default "000000" for test mode)
            
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("Starting to fill Lemon Squeezy payment form...")
        print("=" * 60)
        
        # Wait for page to load
        time.sleep(3)
        
        # Enter email (may be in iframe)
        self.enter_email(email)
        
        # Enter Link OTP code if prompted (in test mode, just enter 000000 directly)
        # No need to click "Send code to email" - just enter the test code
        #self.enter_link_otp_code(otp_code)
        
        # Enter card details in payment element
        self.enter_card_details_in_payment_element(card_number, exp_date, cvc)
        
        # Enter cardholder name
        self.enter_cardholder_name(name)
        
        # Select country
        self.select_country(country)
        
        # Enter billing address
        self.enter_billing_address(address, city, postal_code, state)
        
        print("=" * 60)
        print("Form filling completed!")
        print("=" * 60)
        
        return True
    
    def fill_and_submit(self, email, card_number, exp_date, cvc, name, 
                       country="US", address="123 Main St", city="New York", 
                       postal_code="10001", state=None, otp_code="000000",
                       wait_for_redirect=True, redirect_timeout=30):
        """
        Fill the complete form and submit it, then wait for redirect
        
        Args:
            email: Email address
            card_number: Card number
            exp_date: Expiry date (MMYY)
            cvc: CVC code
            name: Cardholder name
            country: Country code (default "US")
            address: Street address
            city: City name
            postal_code: ZIP/Postal code
            state: State/Province (optional)
            otp_code: OTP code for Link authentication (default "000000" for test mode)
            wait_for_redirect: Whether to wait for redirect after payment (default True)
            redirect_timeout: Seconds to wait for redirect (default 30)
            
        Returns:
            True if form filled and submitted successfully, False otherwise
        """
        # Fill the form
        success = self.fill_complete_form(email, card_number, exp_date, cvc, name,
                                          country, address, city, postal_code, state, otp_code)
        
        if not success:
            print("❌ Form filling failed")
            return False
        
        # Wait a moment for any final processing
        time.sleep(2)
        
        # Submit the form
        print("\n" + "=" * 60)
        print("Submitting payment...")
        print("=" * 60)
        
        return self.submit_form(wait_for_redirect, redirect_timeout)
    
    def submit_form(self, wait_for_redirect=True, redirect_timeout=30):
        """
        Submit the payment form and optionally wait for redirect
        
        Args:
            wait_for_redirect: Whether to wait for page redirect after submission (default True)
            redirect_timeout: Maximum seconds to wait for redirect (default 30)
        
        Returns:
            True if submit successful (and redirect detected if waiting), False otherwise
        """
        try:
            self.driver.switch_to.default_content()
            time.sleep(2)  # Wait a bit to ensure form is ready
            
            print("Looking for Pay button...")
            
            # Try to find submit button by dusk attribute
            button = None
            try:
                button = self.wait_for_clickable(By.CSS_SELECTOR, "[dusk='checkout-form-submit']", timeout=5)
                if button and button.is_enabled():
                    print("Found Pay button by dusk attribute")
                else:
                    button = None
            except:
                pass
            
            # Try to find by text content
            if not button:
                try:
                    button = self.wait_for_clickable(By.XPATH, "//button[contains(text(), 'Pay')]", timeout=5)
                    if button and button.is_enabled():
                        print("Found Pay button by text content")
                except:
                    pass
            
            # Try to find by type=button with Pay text
            if not button:
                try:
                    button = self.wait_for_clickable(By.XPATH, "//button[@type='button' and contains(., 'Pay')]", timeout=5)
                    if button and button.is_enabled():
                        print("Found Pay button by type and text")
                except:
                    pass
            
            if not button:
                print("❌ Submit button not found or not enabled")
                print("   Make sure all form fields are filled correctly")
                return False
            
            # Get current URL before clicking
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            
            # Click the button
            print("Clicking Pay button...")
            button.click()
            print("✅ Pay button clicked!")
            
            if wait_for_redirect:
                print(f"Waiting for redirect (timeout: {redirect_timeout}s)...")
                
                # Wait for URL to change
                try:
                    WebDriverWait(self.driver, redirect_timeout).until(
                        lambda driver: driver.current_url != current_url
                    )
                    new_url = self.driver.current_url
                    print(f"✅ Redirect detected!")
                    print(f"New URL: {new_url}")
                    
                    # Check if redirect looks successful
                    if "success" in new_url.lower() or "thank" in new_url.lower() or "confirmation" in new_url.lower():
                        print("🎉 Payment appears successful!")
                    else:
                        print("⚠️  Redirected to: " + new_url)
                    
                    return True
                    
                except TimeoutException:
                    print(f"⚠️  No redirect detected after {redirect_timeout}s")
                    print("   Payment may still be processing or there may be an error")
                    return False
            else:
                time.sleep(2)  # Brief pause
                return True
            
        except Exception as e:
            print(f"❌ Error submitting form: {e}")
            return False
    
    def close(self):
        """Close the WebDriver if it was created by this bot"""
        if self.own_driver and self.driver:
            self.driver.quit()


# Example usage
if __name__ == "__main__":
    # Lemon Squeezy checkout URL
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    
    # Test card numbers for Stripe
    TEST_CARD = "4242424242424242"
    
    # Create bot instance
    bot = LemonSqueezyBot()
    
    try:
        # Navigate to checkout page
        print(f"Navigating to: {CHECKOUT_URL}")
        bot.driver.get(CHECKOUT_URL)
        
        # Fill complete form
        bot.fill_complete_form(
            email="test@example.com",
            card_number=TEST_CARD,
            exp_date="1225",  # December 2025
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001"
        )
        
        # Optional: Submit the form
        # bot.submit_form()
        
        # Keep browser open for inspection
        print("\n" + "=" * 60)
        print("Form filled! Review the form before submitting.")
        print("=" * 60)
        input("Press Enter to close the browser...")
        
    finally:
        bot.close()
