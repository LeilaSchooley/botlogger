"""
Example: Handling Stripe Link OTP Authentication in Lemon Squeezy
This shows how to handle the OTP code that appears after entering email
"""

from lemonsqueezy_bot import LemonSqueezyBot
import time


def example_with_otp():
    """Example showing OTP code entry (for Stripe Link authentication)"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("Lemon Squeezy Bot - With OTP Authentication")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        # Navigate to checkout
        print("Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # Method 1: Use fill_complete_form with OTP
        print("\n=== Method 1: All-in-one form filling (includes OTP) ===")
        bot.fill_complete_form(
            email="test@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            otp_code="000000"  # In test mode, always use 000000
        )
        
        print("\n" + "=" * 60)
        print("✅ Form filled with OTP authentication!")
        print("=" * 60)
        
        input("\nPress Enter to close...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to close...")
    
    finally:
        bot.close()


def example_step_by_step_with_otp():
    """Example showing step-by-step filling including OTP"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("Step-by-Step Example with OTP")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        # Navigate
        print("Step 1: Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # Enter email
        print("\nStep 2: Entering email...")
        bot.enter_email("test@example.com")
        time.sleep(1)
        
        # Handle OTP prompt
        print("\nStep 3: Entering OTP code (000000 for test mode)...")
        bot.enter_link_otp_code("000000")
        time.sleep(2)
        
        # Enter card details
        print("\nStep 4: Entering card details...")
        bot.enter_card_details_in_payment_element(TEST_CARD, "1225", "123")
        time.sleep(1)
        
        # Enter name
        print("\nStep 5: Entering cardholder name...")
        bot.enter_cardholder_name("John Doe")
        time.sleep(1)
        
        # Select country
        print("\nStep 6: Selecting country...")
        bot.select_country("US")
        time.sleep(1)
        
        # Enter address
        print("\nStep 7: Entering billing address...")
        bot.enter_billing_address("123 Main St", "New York", "10001")
        
        print("\n" + "=" * 60)
        print("✅ All steps completed!")
        print("=" * 60)
        
        input("\nPress Enter to close...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")
    
    finally:
        bot.close()


def example_minimal():
    """Simplest example - just fill the form with OTP"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("Example: Minimal - One Command Does Everything")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        print("Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # One command fills everything including OTP!
        print("\nFilling complete form (including OTP)...")
        bot.fill_complete_form(
            email="test@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            otp_code="000000"  # Test mode: always 000000
        )
        
        print("\n" + "=" * 60)
        print("✅ Done! Form filled automatically!")
        print("=" * 60)
        print("\nThe bot automatically:")
        print("  1. Entered email")
        print("  2. Entered OTP code (000000)")
        print("  3. Filled all card details")
        print("  4. Completed billing address")
        
        input("\nPress Enter to close...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to close...")
    
    finally:
        bot.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LEMON SQUEEZY - OTP AUTHENTICATION EXAMPLES")
    print("=" * 60)
    print("\n📌 KEY POINT: In test mode, OTP is always 000000")
    print("   Just enter it directly - no email sending needed!")
    print("\nChoose an example:")
    print("1. Minimal - One command (recommended)")
    print("2. Complete form with OTP")
    print("3. Step-by-step with OTP")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-3): ").strip()
    
    if choice == "1":
        example_minimal()
    elif choice == "2":
        example_with_otp()
    elif choice == "3":
        example_step_by_step_with_otp()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice!")
