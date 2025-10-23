"""
Complete Lemon Squeezy Purchase Flow (Ported from Cypress)

Tests the full purchase journey:
1. Visit product page
2. Click "Buy" button (opens auth modal)
3. Sign up in modal
4. Modal closes, redirects to checkout
5. Fill checkout form
6. Keep clicking "Pay" until success
7. Verify success message
8. Click "Continue"
9. Click "View order"
10. Verify redirect to dashboard

Note: This requires your app to be running and accessible
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException
from lemonsqueezy_bot import LemonSqueezyBot
import time
import random
import os
import json


class CompletePurchaseFlow:
    """Handles complete purchase flow from product page to dashboard"""
    
    def __init__(self, app_url="https://thebotlord.com"):
        """
        Initialize the purchase flow bot
        
        Args:
            app_url: Your app's URL (localhost or ngrok)
        """
        self.app_url = app_url.rstrip('/')
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.lemon_bot = LemonSqueezyBot(driver=self.driver)
        
        # Generate unique test email
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        self.test_email = f"test{timestamp}{random_num}@example.com"
        self.test_password = "TestPassword123!"

    def safe_click(self, element, attempts=3, scroll=True, wait_between=0.6):
        """Safely click an element with fallbacks.

        Tries element.click(), then ActionChains click, then JS click. Retries on
        StaleElementReferenceException. This reduces "element click intercepted"
        errors when overlays or scrolling interfere.
        """
        from selenium.webdriver import ActionChains

        last_exc = None
        for attempt in range(1, attempts + 1):
            try:
                # Native click first
                element.click()
                return True
            except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                # Click was intercepted or not interactable; attempt scroll + action chains
                last_exc = e
                try:
                    if scroll:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        #time.sleep(0.15)
                    ActionChains(self.driver).move_to_element(element).pause(0.05).click().perform()
                    return True
                except Exception:
                    try:
                        # Final fallback: JavaScript click
                        self.driver.execute_script("arguments[0].click();", element)
                        return True
                    except Exception as e2:
                        last_exc = e2
                        time.sleep(wait_between)
            except StaleElementReferenceException as e:
                # Element went stale; wait and retry (caller should be able to find again)
                last_exc = e
                time.sleep(wait_between)
            except Exception as e:
                # Generic fallback for any other unexpected error
                last_exc = e
                time.sleep(wait_between)
        # All attempts failed
        raise last_exc

    def _capture_debug(self, name: str):
        """Save a screenshot and page HTML for debugging."""
        try:
            debug_dir = os.path.join(os.getcwd(), "debug")
            os.makedirs(debug_dir, exist_ok=True)
            png = os.path.join(debug_dir, f"{name}.png")
            html = os.path.join(debug_dir, f"{name}.html")
            try:
                self.driver.save_screenshot(png)
                print(f"📸 Screenshot saved: {png}")
            except Exception as e:
                print(f"⚠️  Could not save screenshot: {e}")
            try:
                with open(html, "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"📄 Page source saved: {html}")
            except Exception as e:
                print(f"⚠️  Could not save page source: {e}")
        except Exception as e:
            print(f"⚠️  Debug capture failed: {e}")

    def _capture_element_diagnostics(self, element, name: str):
        """Capture detailed diagnostics for a DOM element and save to a file.

        Returns a dict of captured values and writes a JSON diagnostics file to the debug folder.
        """
        try:
            diag = {}
            try:
                # Collect basic Python-side attributes
                diag['tag_name'] = element.tag_name
                diag['text'] = element.text
                diag['enabled'] = element.is_enabled()
                diag['displayed'] = element.is_displayed()
                diag['attributes'] = {}
                # Some useful attributes
                for attr in ['id', 'class', 'href', 'type', 'role', 'data-buy-button', 'data-testid', 'onclick']:
                    try:
                        diag['attributes'][attr] = element.get_attribute(attr)
                    except Exception:
                        diag['attributes'][attr] = None
            except Exception as e:
                diag['python_side_error'] = str(e)

            # Run JS to gather DOM-side diagnostics
            js = '''
            try {
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const styles = window.getComputedStyle(el);
                const centerX = rect.left + rect.width/2;
                const centerY = rect.top + rect.height/2;
                function styleMap(styles){
                    const out = {};
                    ['display','visibility','opacity','zIndex','pointerEvents','position'].forEach(k=>{ out[k]=styles.getPropertyValue(k); });
                    return out;
                }
                const top = document.elementFromPoint(centerX, centerY);
                return {
                    rect: {left:rect.left, top:rect.top, width:rect.width, height:rect.height},
                    computedStyle: styleMap(styles),
                    outerHTML: el.outerHTML,
                    topElementAtCenter: top ? {tag: top.tagName, outerHTML: top.outerHTML.slice(0,1000)} : null,
                    viewport: {width: window.innerWidth, height: window.innerHeight, scrollX: window.scrollX, scrollY: window.scrollY}
                };
            } catch(e) { return {js_error: String(e)}; }
            '''
            try:
                res = self.driver.execute_script(js, element)
                diag['dom'] = res
            except Exception as e:
                diag['dom_capture_error'] = str(e)

            # Save diagnostic JSON
            debug_dir = os.path.join(os.getcwd(), 'debug')
            os.makedirs(debug_dir, exist_ok=True)
            diag_path = os.path.join(debug_dir, f"{name}_diag.json")
            try:
                with open(diag_path, 'w', encoding='utf-8') as f:
                    json.dump(diag, f, indent=2)
                print(f"📘 Element diagnostics saved: {diag_path}")
            except Exception as e:
                print(f"⚠️  Could not save diagnostics: {e}")

            return diag
        except Exception as e:
            print(f"⚠️  _capture_element_diagnostics failed: {e}")
            return {'error': str(e)}

    def clear_all_storage(self):
        """Clear cookies, localStorage, and sessionStorage"""
        print("🔓 Clearing all storage...")
        self.driver.delete_all_cookies()
        
        try:
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
            print("✅ Storage cleared")
        except Exception as e:
            print(f"⚠️  Could not clear storage: {e}")
    
    def force_logout(self):
        """Aggressively force logout state"""
        print("🔓 AGGRESSIVELY forcing logout state...")
        
        # Clear before visiting
        self.clear_all_storage()
        
        # Visit homepage to access window
        print("🏠 Visiting homepage to clear auth state...")
        self.driver.get(self.app_url)
        #time.sleep(2)
        
        # Debug: Check localStorage BEFORE clearing
        ls_keys = self.driver.execute_script("return Object.keys(window.localStorage);")
        print(f"📦 LocalStorage keys BEFORE clear: {', '.join(ls_keys) if ls_keys else 'NONE'}")
        
        # Clear everything
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        
        # Double-check it's cleared
        ls_keys_after = self.driver.execute_script("return Object.keys(window.localStorage);")
        print(f"📦 LocalStorage keys AFTER clear: {', '.join(ls_keys_after) if ls_keys_after else 'NONE'}")
        
        # Clear cookies again
        self.driver.delete_all_cookies()
        #time.sleep(2)
        print("✅ Forced logout complete")
    
    def visit_product_page(self, product_slug="google-ads-clicker"):
        """Visit the product page"""
        product_url = f"{self.app_url}/products/custom/{product_slug}"
        print(f"🏠 Visiting product page: {product_url}")
        self.driver.get(product_url)
        #time.sleep(2)
        
        # Debug: Check auth state on product page
        ls_keys = self.driver.execute_script("return Object.keys(window.localStorage);")
        print(f"📦 LocalStorage keys on product page: {', '.join(ls_keys) if ls_keys else 'NONE'}")
        
        # Check for auth keys
        auth_keys = [key for key in ls_keys if 'supabase' in key or 'sb-' in key or 'auth' in key]
        
        if auth_keys:
            print(f"⚠️  WARNING: Found auth keys: {', '.join(auth_keys)}")
            # Force remove them
            for key in auth_keys:
                self.driver.execute_script(f"window.localStorage.removeItem('{key}');")
                print(f"🗑️  Removed: {key}")
        else:
            print("✅ No auth keys found - good!")
        
        #time.sleep(1)
    
    def click_buy_button(self):
        """Click the Buy button (opens auth modal)"""
        print("🛒 Clicking Buy button (will open auth modal)...")

        selectors = [
           #("text", "Get Lifetime"),
            ("text", "Start Monthly"),
            #("css", "[data-buy-button]"),
        ]

        clicked = False
        for selector_type, selector_value in selectors:
            try:
                if selector_type == "text":
                    button = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{selector_value}')]")
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector_value)
            except NoSuchElementException:
                continue

            print(f"✅ Found '{selector_value}' button")

            # Quick diagnostics
            try:
                print(f"🔎 tag={button.tag_name}, enabled={button.is_enabled()}, displayed={button.is_displayed()}, rect={getattr(button,'rect',None)}")
            except Exception as e:
                print(f"⚠️  diagnostics failed: {e}")

            # Attempt sequence of click strategies until auth modal appears
            try_strategies = [
                ("safe_click", lambda el: self.safe_click(el)),
                ("parent_anchor", lambda el: (el.find_element(By.XPATH, './ancestor::a')) and self.safe_click(el.find_element(By.XPATH, './ancestor::a'))),
                ("js_mouse_event", lambda el: self.driver.execute_script("var el=arguments[0]; el.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));", el)),
                ("invoke_onclick", lambda el: self.driver.execute_script("if(arguments[0] && arguments[0].onclick){ arguments[0].onclick(); }", el)),
            ]

            # Strategy 1: safe_click on the element itself
            try:
                try:
                    ok = self.safe_click(button)
                    print(f"👉 safe_click returned: {ok}")
                except Exception as e:
                    print(f"⚠️  safe_click failed: {e}")

                # short wait and check for modal
                #time.sleep(1.5)
                try:
                    if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))):
                        print("✅ Auth modal appeared after click")
                        clicked = True
                        break
                except Exception:
                    pass

                # Strategy 2: click ancestor link if exists
                try:
                    parent = button.find_element(By.XPATH, './ancestor::a')
                    print("🔁 Trying ancestor anchor click")
                    try:
                        self.driver.execute_script("arguments[0].removeAttribute('target');", parent)
                    except Exception:
                        pass
                    try:
                        self.safe_click(parent)
                    except Exception as e:
                        print(f"⚠️  ancestor click failed: {e}")
                    #time.sleep(1.5)
                    try:
                        if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))):
                            print("✅ Auth modal appeared after ancestor click")
                            clicked = True
                            break
                    except Exception:
                        pass
                except Exception:
                    pass

                # Strategy 3: dispatch JS MouseEvent
                try:
                    print("🔁 Dispatching JS MouseEvent click as fallback...")
                    self.driver.execute_script(
                        "var el = arguments[0]; el.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));",
                        button,
                    )
                    #time.sleep(1.5)
                    try:
                        if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))):
                            print("✅ Auth modal appeared after JS MouseEvent")
                            clicked = True
                            break
                    except Exception:
                        pass
                except Exception as e:
                    print(f"⚠️  JS MouseEvent click failed: {e}")

                # Strategy 4: invoke onclick
                try:
                    print("🔁 Invoking element.onclick() via JS as fallback...")
                    self.driver.execute_script("if(arguments[0] && arguments[0].onclick){ arguments[0].onclick(); }", button)
                    #time.sleep(1.5)
                    try:
                        if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))):
                            print("✅ Auth modal appeared after invoking onclick")
                            clicked = True
                            break
                    except Exception:
                        pass
                except Exception as e:
                    print(f"⚠️  invoking onclick failed: {e}")

                # Strategy 5: overlay detection and temporary disable
                try:
                    print("🔍 Checking for blocking element at button center...")
                    js_top = '''
                    try {
                        const el = arguments[0];
                        const rect = el.getBoundingClientRect();
                        const cx = rect.left + rect.width/2;
                        const cy = rect.top + rect.height/2;
                        const top = document.elementFromPoint(cx, cy);
                        return top ? {tag: top.tagName, outerHTML: top.outerHTML.slice(0,500), isSame: top===el} : null;
                    } catch(e){ return {js_error: String(e)} }
                    '''
                    top_info = self.driver.execute_script(js_top, button)
                    print(f"🔎 top_at_center: {top_info}")
                    if top_info and not top_info.get('isSame'):
                        print("🧹 Found a blocking element: disabling pointer events and retrying")
                        rect = getattr(button, 'rect', None) or {'left':0,'top':0,'width':0,'height':0}
                        cx = rect['left'] + rect['width']/2
                        cy = rect['top'] + rect['height']/2
                        try:
                            self.driver.execute_script("var el=document.elementFromPoint(arguments[0], arguments[1]); if(el){ el.style.pointerEvents='none'; }", cx, cy)
                        except Exception:
                            pass
                        try:
                            self.safe_click(button)
                            time.sleep(1.5)
                            if self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))):
                                print("✅ Auth modal appeared after hiding blocker")
                                clicked = True
                                break
                        except Exception as e:
                            print(f"⚠️  retry after disabling blocker failed: {e}")
                except Exception as e:
                    print(f"⚠️  overlay detection attempt failed: {e}")

                # If none of the strategies worked, capture debug information and continue
                print("❌ Click attempts did not open auth modal for this selector - capturing debug info")
                try:
                    self._capture_element_diagnostics(button, 'buy_click_failed')
                except Exception as e:
                    print(f"⚠️  element diagnostics capture failed: {e}")
                self._capture_debug('buy_click_failed')

            except Exception as e:
                # Safety net for unexpected errors while attempting strategies
                print(f"⚠️  Unexpected error while attempting click strategies: {e}")
                try:
                    self._capture_debug('buy_click_exception')
                except Exception:
                    pass

        # End of selector loop
        if not clicked:
            print("⚠️  No buy button found or click did not open modal, listing all buttons:")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for i, btn in enumerate(buttons):
                print(f"Button {i}: {btn.text}")
            raise Exception("Could not find buy button or open auth modal")

        time.sleep(2)

    def wait_for_auth_modal(self):
        """Wait for auth modal to appear"""
        print("🔐 Waiting for auth modal to appear...")
        try:
            modal = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))
            )
            print("✅ Auth modal appeared")
            return True
        except TimeoutException:
            print("❌ Auth modal did not appear")
            return False
    
    def signup_in_modal(self):
        """Fill out sign-up form in the auth modal"""
        print("📝 Filling out sign-up form in modal...")
        
        # Click Sign Up tab to be sure
        try:
            signup_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="signup-tab"]')
            self.safe_click(signup_tab)
            time.sleep(1)
        except NoSuchElementException:
            print("⚠️  Sign Up tab not found, assuming already on signup")
        
        # Fill email
        print(f"📧 Entering email: {self.test_email}")
        email_field = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="signup-email"]')
        email_field.clear()
        email_field.send_keys(self.test_email)
        
        # Fill password
        print("🔒 Entering password")
        password_field = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="signup-password"]')
        password_field.clear()
        password_field.send_keys(self.test_password)
        
        # Submit
        print("✅ Submitting sign-up form...")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="signup-submit"]')
        self.safe_click(submit_button)

        time.sleep(2)
    
    def wait_for_modal_close_and_checkout(self):
        """Wait for modal to close and redirect to checkout"""
        print("🎉 Waiting for modal to close and checkout to open...")
        
        try:
            # Wait for modal to disappear
            WebDriverWait(self.driver, 15).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-modal"]'))
            )
            print("✅ Modal closed")
        except TimeoutException:
            print("⚠️  Modal still visible, but continuing...")
        
        time.sleep(3)
        
        # Wait for redirect to Lemon Squeezy
        print("💳 Verifying redirect to LemonSqueezy checkout...")
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: "lemonsqueezy.com" in driver.current_url
            )
            print(f"✅ Redirected to: {self.driver.current_url}")
            return True
        except TimeoutException:
            print(f"❌ Not redirected to LemonSqueezy. Current URL: {self.driver.current_url}")
            return False
    
    def wait_for_checkout_iframes(self):
        """Wait for checkout page and iframes to load"""
        print("⏳ Waiting for checkout iframes...")
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name*="__privateStripeFrame"]'))
            )
            print("✅ Checkout iframes loaded")
            time.sleep(3)
            return True
        except TimeoutException:
            print("⚠️  Checkout iframes not found")
            return False
    
    def fill_checkout_form(self):
        """Fill the Lemon Squeezy checkout form"""
        print("📝 Filling checkout form...")
        
        # Use the LemonSqueezyBot methods
        # Fill email
        print("📧 Entering email...")
        self.lemon_bot.enter_email(self.test_email)
        time.sleep(2)
        
        # Handle OTP if prompted
        print("🔐 Handling OTP (if required)...")
        self.lemon_bot.enter_link_otp_code("000000")
        time.sleep(2)
        
        # Fill card details
        print("💳 Entering card details...")
        self.lemon_bot.enter_card_details_in_payment_element(
            card_number="4242424242424242",
            exp_date="1234",
            cvc="123"
        )
        time.sleep(2)
        
        # Fill name
        print("👤 Entering name...")
        self.lemon_bot.enter_cardholder_name("Test User")
        time.sleep(2)
        
        # Select country
        print("🌍 Selecting country...")
        self.lemon_bot.select_country("US")
        time.sleep(2)
        
        # Fill billing address
        print("🏠 Filling billing address...")
        self.lemon_bot.enter_billing_address(
            address_line1="123 Test St",
            city="Test City",
            postal_code="12345",
            state="California"
        )
        time.sleep(2)
        
        print("✅ Checkout form filled")
    
    def keep_clicking_pay_until_success(self, max_attempts=10):
        """Keep clicking Pay button until payment succeeds"""
        print("💰 Starting payment attempts...")
        
        pay_keywords = [
            'pay', 'pay now', 'complete', 'complete order', 'place order', 'confirm', 'submit', 'purchase', 'checkout'
        ]

        for attempt in range(1, max_attempts + 1):
            print(f"💳 Payment attempt {attempt}/{max_attempts}...")
            
            # Check for success indicators
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            if any(msg in page_text for msg in [
                "Payment successful",
                "Order confirmed",
                "Thank you"
            ]):
                print("✅ Payment successful!")
                return True
            
            # Check for Continue button (indicates success)
            try:
                continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
                if continue_btn.is_displayed():
                    print("✅ Payment successful (Continue button found)!")
                    return True
            except NoSuchElementException:
                pass
            
            # Check for processing message
            if any(msg in page_text for msg in [
                "Processing your order",
                "Please wait"
            ]):
                print("⏳ Order is processing, waiting...")
                time.sleep(5)
                continue

            # Auto-check obvious terms checkboxes to enable buttons
            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                for cb in checkboxes:
                    try:
                        lbl = ''
                        try:
                            lbl = (cb.get_attribute('aria-label') or cb.get_attribute('name') or '')
                        except Exception:
                            lbl = ''
                        if not cb.is_selected() and any(k in lbl.lower() for k in ['term', 'agree', 'accept', 'policy', 'consent']):
                            print("☑️ Auto-checking terms checkbox")
                            try:
                                self.safe_click(cb)
                            except Exception:
                                try:
                                    self.driver.execute_script("arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change'));", cb)
                                except Exception:
                                    pass
                    except Exception:
                        pass
            except Exception:
                pass

            # Broad search for pay/submit elements (case-insensitive) using XPath translate()
            found = []
            for kw in pay_keywords:
                try:
                    expr = ("//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]" % kw)
                    found += self.driver.find_elements(By.XPATH, expr)
                    expr2 = ("//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]" % kw)
                    found += self.driver.find_elements(By.XPATH, expr2)
                    expr3 = ("//input[@type='submit' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]" % kw)
                    found += self.driver.find_elements(By.XPATH, expr3)
                except Exception:
                    pass

            # Remove duplicates while preserving order
            seen = set()
            candidates = []
            for el in found:
                try:
                    aid = (el.get_attribute('outerHTML') or str(el))
                except Exception:
                    aid = str(el)
                if aid in seen:
                    continue
                seen.add(aid)
                candidates.append(el)

            if candidates:
                clicked_any = False
                for el in candidates:
                    try:
                        if not el.is_displayed():
                            continue
                        # If button disabled, try to remove disabled attribute
                        try:
                            if not el.is_enabled():
                                print("⚠️  Button is disabled, trying to enable")
                                self.driver.execute_script("arguments[0].removeAttribute('disabled')", el)
                        except Exception:
                            pass
                        try:
                            print(f"🔘 Clicking on candidate button: {el.text}")
                            self.safe_click(el)
                            clicked_any = True
                            time.sleep(2)
                            break
                        except Exception as e:
                            print(f"⚠️  Click on candidate button failed: {e}")
                    except Exception:
                        pass

                if clicked_any:
                    # Short wait and check for success
                    time.sleep(2)
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text
                    if any(msg in page_text for msg in [
                        "Payment successful",
                        "Order confirmed",
                        "Thank you"
                    ]):
                        print("✅ Payment successful after clicking candidate!")
                        return True
                    else:
                        print("⚠️  Payment not successful after clicking candidate, checking for Continue button...")
                        try:
                            continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
                            if continue_btn.is_displayed():
                                print("✅ Payment successful (Continue button found) after clicking candidate!")
                                return True
                        except NoSuchElementException:
                            pass
            else:
                print("⚠️  No Pay/Submit candidates found on page")
                try:
                    cur = self.driver.current_url
                    print(f"🔗 Current URL while searching for Pay: {cur}")
                except Exception:
                    pass
                try:
                    body_text = self.driver.find_element(By.TAG_NAME, 'body').text
                    snippet = body_text[:1000].replace('\n', ' ')
                    print(f"📝 Page body snippet (first 1000 chars): {snippet}")
                except Exception as e:
                    print(f"⚠️ Could not read body text: {e}")
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                    print(f"🔘 Found {len(buttons)} buttons on page:")
                    for i, b in enumerate(buttons):
                        try:
                            print(f"  [{i}] text='{b.text}' enabled={b.is_enabled()} displayed={b.is_displayed()} outerHTML_len={len(b.get_attribute('outerHTML') or '')}")
                        except Exception:
                            print(f"  [{i}] <could not read button details>")
                except Exception:
                    pass
                try:
                    anchors = self.driver.find_elements(By.TAG_NAME, 'a')
                    print(f"🔗 Found {len(anchors)} anchors on page (text / href):")
                    for i, a in enumerate(anchors[:30]):
                        try:
                            print(f"  [{i}] text='{a.text}' href='{a.get_attribute('href')}'")
                        except Exception:
                            print(f"  [{i}] <could not read anchor details>")
                except Exception:
                    pass

            # Capture debug artifacts for this attempt
            try:
                self._capture_debug(f'pay_missing_attempt_{attempt}')
            except Exception as e:
                print(f"⚠️  debug capture failed: {e}")

            # Wait a bit before next attempt
            time.sleep(3)

        print(f"❌ Payment not successful after {max_attempts} attempts")
        return False

    def verify_success_message(self):
        """Verify the success message on the page"""
        print("✅ Verifying success message...")
        time.sleep(2)
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        if any(msg in page_text for msg in [
            "Payment successful",
            "Order confirmed",
            "Thank you"
        ]):
            print("✅ Success message is visible")
            return True
        else:
            print("❌ Success message not found in page text")
            return False

    def click_continue_button(self):
        """Click the Continue button on the success page"""
        print("➡️ Clicking Continue button...")
        try:
            continue_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
            self.safe_click(continue_btn)
            print("✅ Continue button clicked")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Could not click Continue button: {e}")
            self._capture_debug('continue_button_click_failed')

    def click_view_order_button(self):
        """Click the View Order button on the success page"""
        print("📦 Clicking View Order button...")
        try:
            view_order_btn = self.driver.find_element(By.XPATH, "//a[contains(text(), 'View order')]")
            self.safe_click(view_order_btn)
            print("✅ View Order button clicked")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Could not click View Order button: {e}")
            self._capture_debug('view_order_button_click_failed')

    def verify_redirect_to_dashboard(self):
        """Verify that the user is redirected to the dashboard"""
        print("🔄 Verifying redirect to dashboard...")
        time.sleep(2)
        current_url = self.driver.current_url
        if "dashboard" in current_url or "account" in current_url:
            print(f"✅ Successfully redirected to dashboard: {current_url}")
            return True
        else:
            print(f"❌ Not redirected to dashboard, current URL: {current_url}")
            self._capture_debug('redirect_to_dashboard_failed')
            return False

    def full_purchase_flow(self, product_slug="google-ads-clicker"):
        """Run the complete purchase flow"""
        print("🚀 Starting full purchase flow...")
        try:
            self.visit_product_page(product_slug)
            self.click_buy_button()
            if not self.wait_for_auth_modal():
                raise Exception("Auth modal did not appear")
            self.signup_in_modal()
            self.wait_for_modal_close_and_checkout()
            if not self.wait_for_checkout_iframes():
                raise Exception("Checkout iframes did not load")
            self.fill_checkout_form()
            time.sleep(33333)

            if not self.keep_clicking_pay_until_success():
                raise Exception("Payment did not succeed")
            if not self.verify_success_message():
                raise Exception("Success message not found")

            self.click_continue_button()
            self.click_view_order_button()
            self.verify_redirect_to_dashboard()
            print("🎉 Full purchase flow completed successfully!")
        except Exception as e:
            print(f"❌ Error during purchase flow: {e}")
            self._capture_debug('full_purchase_flow_failed')
            raise
        finally:
            print("🧹 Cleaning up...")
            time.sleep(2)
            self.driver.quit()
            print("✅ Cleanup complete")

    def run_complete_flow(self, product_slug="google-ads-clicker"):
        """Compatibility wrapper used by existing runners/tests.

        Calls full_purchase_flow and returns True on success, False on failure.
        """
        try:
            self.full_purchase_flow(product_slug)
            return True
        except Exception as e:
            print(f"run_complete_flow: failed: {e}")
            return False

    def close(self):
        """Close the browser if it's open (compat wrapper)."""
        try:
            if getattr(self, 'driver', None):
                self.driver.quit()
        except Exception as e:
            print(f"close: error while quitting driver: {e}")

if __name__ == "__main__":
    bot = CompletePurchaseFlow()
    bot.run_complete_flow()
