"""
Example usage of the Stripe Card Bot
Demonstrates different ways to use the bot
"""

from stripe_card_bot import StripeCardBot
import time


def example_basic_usage():
    """Basic usage example - fill all fields at once"""
    print("\n" + "="*60)
    print("Example 1: Basic Usage - Fill All Fields")
    print("="*60 + "\n")
    
    bot = StripeCardBot()
    
    try:
        # Navigate to your payment page
        # Replace with your actual payment page URL
        bot.driver.get("https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636")
        print("Navigate to your payment page first!")
        print("Uncomment the line above and add your URL")
        
        # Fill all card details
        bot.fill_card_details(
            card_number="4242 4242 4242 4242",  # Stripe test card (success)
            exp_date="1225",                     # December 2025
            cvc="123",
            name="John Doe",
            zip_code="12345"
        )
        
        # Optional: Submit the form
        # bot.submit_form()
        
        print("\nTest completed! Check the browser.")
        input("Press Enter to close browser...")
        
    finally:
        bot.close()


def example_step_by_step():
    """Step-by-step example - fill fields individually"""
    print("\n" + "="*60)
    print("Example 2: Step-by-Step - Individual Fields")
    print("="*60 + "\n")
    
    bot = StripeCardBot()
    
    try:
        # Navigate to payment page
        # bot.driver.get("https://your-payment-page.com")
        
        print("Step 1: Entering card number...")
        bot.enter_card_number("4242 4242 4242 4242")
        time.sleep(1)
        
        print("Step 2: Entering expiry date...")
        bot.enter_expiry_date("1225")
        time.sleep(1)
        
        print("Step 3: Entering CVC...")
        bot.enter_cvc("123")
        time.sleep(1)
        
        print("Step 4: Entering cardholder name...")
        bot.enter_cardholder_name("Jane Smith")
        time.sleep(1)
        
        print("\nAll fields filled step-by-step!")
        input("Press Enter to close browser...")
        
    finally:
        bot.close()


def example_with_custom_driver():
    """Example using a custom configured WebDriver"""
    print("\n" + "="*60)
    print("Example 3: Custom WebDriver Configuration")
    print("="*60 + "\n")
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    # Configure Chrome options
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Create driver
    driver = webdriver.Chrome(options=options)
    
    # Create bot with custom driver
    bot = StripeCardBot(driver=driver)
    
    try:
        # Navigate to payment page
        # driver.get("https://your-payment-page.com")
        
        # Fill card details
        bot.fill_card_details(
            card_number="5555 5555 5555 4444",  # Mastercard test card
            exp_date="0626",                     # June 2026
            cvc="456",
            name="Custom Driver User"
        )
        
        print("\nTest completed with custom driver!")
        input("Press Enter to close browser...")
        
    finally:
        driver.quit()


def example_test_multiple_cards():
    """Example testing multiple card scenarios"""
    print("\n" + "="*60)
    print("Example 4: Testing Multiple Card Scenarios")
    print("="*60 + "\n")
    
    # Different Stripe test cards
    test_scenarios = [
        {
            "name": "Successful Visa",
            "card": "4242 4242 4242 4242",
            "exp": "1225",
            "cvc": "123"
        },
        {
            "name": "Declined Card",
            "card": "4000 0000 0000 0002",
            "exp": "1225",
            "cvc": "123"
        },
        {
            "name": "Successful Mastercard",
            "card": "5555 5555 5555 4444",
            "exp": "1225",
            "cvc": "123"
        }
    ]
    
    bot = StripeCardBot()
    
    try:
        # Navigate to payment page
        # bot.driver.get("https://your-payment-page.com")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n--- Test {i}: {scenario['name']} ---")
            
            bot.fill_card_details(
                card_number=scenario['card'],
                exp_date=scenario['exp'],
                cvc=scenario['cvc'],
                name=f"Test User {i}"
            )
            
            # In real scenario, you might submit and check result
            # bot.submit_form()
            # time.sleep(2)
            # Check for success/error messages
            
            if i < len(test_scenarios):
                print(f"\nPreparing for next test scenario...")
                time.sleep(2)
                # In real scenario, navigate back to payment page
                # bot.driver.get("https://your-payment-page.com")
        
        print("\n" + "="*60)
        print("All test scenarios completed!")
        print("="*60)
        input("\nPress Enter to close browser...")
        
    finally:
        bot.close()


def example_debug_iframes():
    """Example for debugging - find which iframes contain elements"""
    print("\n" + "="*60)
    print("Example 5: Debug - Find Stripe iframes")
    print("="*60 + "\n")
    
    bot = StripeCardBot()
    
    try:
        # Navigate to your payment page
        # bot.driver.get("https://your-payment-page.com")
        
        print("Searching for card number field in all iframes...")
        bot.find_stripe_iframe_with_element("cardnumber")
        
        print("\nSearching for expiry date field in all iframes...")
        bot.find_stripe_iframe_with_element("exp-date")
        
        print("\nSearching for CVC field in all iframes...")
        bot.find_stripe_iframe_with_element("cvc")
        
        print("\nDebug information collected!")
        input("Press Enter to close browser...")
        
    finally:
        bot.close()


def main():
    """Main function - choose which example to run"""
    print("\n" + "="*60)
    print("Stripe Card Bot - Examples")
    print("="*60)
    print("\nChoose an example to run:")
    print("1. Basic Usage - Fill all fields at once")
    print("2. Step-by-Step - Fill fields individually")
    print("3. Custom WebDriver - Use your own driver configuration")
    print("4. Multiple Cards - Test different card scenarios")
    print("5. Debug Mode - Find iframe locations")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    examples = {
        '1': example_basic_usage,
        '2': example_step_by_step,
        '3': example_with_custom_driver,
        '4': example_test_multiple_cards,
        '5': example_debug_iframes
    }
    
    if choice == '0':
        print("Exiting...")
        return
    
    example_func = examples.get(choice)
    if example_func:
        example_func()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("IMPORTANT: Before running these examples")
    print("="*60)
    print("1. Make sure you have Selenium installed:")
    print("   pip install selenium")
    print("\n2. Uncomment the bot.driver.get() lines in the examples")
    print("   and replace with your actual payment page URL")
    print("\n3. These examples use Stripe test cards that won't charge")
    print("   real money. See README_STRIPE_BOT.md for more test cards")
    print("="*60 + "\n")
    
    input("Press Enter to continue...")
    
    main()
