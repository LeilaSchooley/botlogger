"""
Complete End-to-End Example: Fill form, submit, and wait for redirect
This example demonstrates the full payment flow including submission
"""

from lemonsqueezy_bot import LemonSqueezyBot
import time


def complete_checkout_with_submit():
    """Complete checkout flow: fill form, submit, wait for redirect"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("COMPLETE CHECKOUT FLOW - WITH SUBMISSION")
    print("=" * 60)
    print("\nThis bot will:")
    print("  1. Fill all form fields")
    print("  2. Enter OTP code (000000)")
    print("  3. Click the Pay button")
    print("  4. Wait for redirect to success page")
    print("\n⚠️  Test mode only - no real charges")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        # Step 1: Navigate to checkout
        print("Step 1: Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        # Step 2: Fill the form (including OTP)
        print("\nStep 2: Filling form...")
        success = bot.fill_complete_form(
            email="test@example.com",
            card_number=TEST_CARD,
            exp_date="1225",
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            state="New York",  # Required!
            otp_code="000000"
        )
        
        if not success:
            print("❌ Form filling failed!")
            input("\nPress Enter to close...")
            return
        
        print("✅ Form filled successfully!")
        time.sleep(2)
        
        # Step 3: Submit and wait for redirect
        print("\nStep 3: Submitting payment...")
        print("(Will wait up to 30 seconds for redirect)")
        
        submit_success = bot.submit_form(wait_for_redirect=True, redirect_timeout=30)
        
        if submit_success:
            print("\n" + "=" * 60)
            print("🎉 SUCCESS! Payment completed!")
            print("=" * 60)
            print("\nCheck the browser window for the confirmation page")
        else:
            print("\n" + "=" * 60)
            print("⚠️  Warning: Submit may have issues")
            print("=" * 60)
            print("\nPlease check the browser for any errors")
        
        input("\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to close the browser...")
    
    finally:
        bot.close()


def fill_without_submit():
    """Fill form but don't submit - for manual review"""
    
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("FILL ONLY - NO SUBMISSION")
    print("=" * 60)
    print("\nThis will fill the form but NOT submit")
    print("You can review before manually clicking Pay")
    print("=" * 60 + "\n")
    
    bot = LemonSqueezyBot()
    
    try:
        print("Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        time.sleep(3)
        
        print("\nFilling form...")
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
            state="New York",
            otp_code="000000"
        )
        
        print("\n" + "=" * 60)
        print("✅ Form filled - ready for manual review!")
        print("=" * 60)
        print("\nYou can now:")
        print("  • Review all fields in the browser")
        print("  • Manually click the Pay button if everything looks good")
        print("  • Or just close the browser to cancel")
        
        input("\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to close...")
    
    finally:
        bot.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LEMON SQUEEZY - COMPLETE PAYMENT FLOW")
    print("=" * 60)
    print("\nChoose an option:")
    print("1. Complete flow (fill + submit + wait for redirect)")
    print("2. Fill only (no submission - manual review)")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-2): ").strip()
    
    if choice == "1":
        complete_checkout_with_submit()
    elif choice == "2":
        fill_without_submit()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice!")
