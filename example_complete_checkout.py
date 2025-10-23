"""
Complete Example: Fill form and submit payment automatically
This example shows how to complete an entire checkout flow end-to-end
"""

from lemonsqueezy_bot import LemonSqueezyBot
import time


def example_complete_checkout():
    """Complete checkout flow - fill and submit"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("COMPLETE CHECKOUT FLOW")
    print("=" * 60)
    print("\nThis will:")
    print("  1. Fill all form fields")
    print("  2. Click the Pay button")
    print("  3. Wait for redirect")
    print("  4. Show success page")
    print("\n⚠️  Test mode only - no real charges")
    print("=" * 60 + "\n")
    
    input("Press Enter to start...")
    
    bot = LemonSqueezyBot()
    
    try:
        # Navigate to checkout
        print("\n📍 Step 1: Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # Fill and submit in one command
        print("\n📝 Step 2: Filling form and submitting payment...")
        success = bot.fill_and_submit(
            email="testbuyer@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            otp_code="000000",
            wait_for_redirect=True,
            redirect_timeout=30
        )
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 CHECKOUT COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\n✅ Payment processed")
            print("✅ Redirected to success page")
            print("\nCheck the browser window for the confirmation page.")
        else:
            print("\n" + "=" * 60)
            print("⚠️  CHECKOUT HAD ISSUES")
            print("=" * 60)
            print("\nPlease check the browser for error messages.")
        
        input("\n\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to close...")
    
    finally:
        bot.close()


def example_manual_submit():
    """Fill form first, then manually submit"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("MANUAL SUBMIT EXAMPLE")
    print("=" * 60)
    print("\nThis will:")
    print("  1. Fill the form")
    print("  2. Wait for your confirmation")
    print("  3. Submit when you're ready")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        # Navigate
        print("Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # Fill form only
        print("\nFilling form...")
        bot.fill_complete_form(
            email="testbuyer@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            otp_code="000000"
        )
        
        print("\n✅ Form filled!")
        print("\nReview the form in the browser.")
        
        # Ask for confirmation
        choice = input("\nSubmit the payment? (y/n): ").strip().lower()
        
        if choice == 'y':
            print("\nSubmitting...")
            success = bot.submit_form(wait_for_redirect=True, redirect_timeout=30)
            
            if success:
                print("\n🎉 Payment completed!")
            else:
                print("\n⚠️  Submission had issues")
        else:
            print("\n✋ Cancelled")
        
        input("\nPress Enter to close...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to close...")
    
    finally:
        bot.close()


def example_no_wait():
    """Submit without waiting for redirect"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("SUBMIT WITHOUT WAITING")
    print("=" * 60)
    print("\nThis will click Pay but not wait for redirect.")
    print("Useful if you want to monitor manually.")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        print("Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        print("\nFilling and submitting...")
        bot.fill_and_submit(
            email="testbuyer@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            otp_code="000000",
            wait_for_redirect=False  # Don't wait
        )
        
        print("\n✅ Pay button clicked!")
        print("Monitor the browser for payment processing...")
        
        input("\nPress Enter to close...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to close...")
    
    finally:
        bot.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LEMON SQUEEZY - COMPLETE CHECKOUT EXAMPLES")
    print("=" * 60)
    print("\nChoose an example:")
    print("1. Complete checkout (fill + submit + wait) - RECOMMENDED")
    print("2. Manual submit (fill, review, then submit)")
    print("3. Submit without waiting for redirect")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-3): ").strip()
    
    if choice == "1":
        example_complete_checkout()
    elif choice == "2":
        example_manual_submit()
    elif choice == "3":
        example_no_wait()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice!")
