"""
Example: Using LemonSqueezyBot to automate checkout
"""

from lemonsqueezy_bot import LemonSqueezyBot
import time


def main():
    """Run the Lemon Squeezy bot example"""
    
    # Your Lemon Squeezy checkout URL
    CHECKOUT_URL = "https://the-bot-lord.lemonsqueezy.com/buy/5ffb8fab-5356-4f0d-bad9-bd65b3285636"
    
    # Stripe test card (won't charge real money)
    TEST_CARD = "4242424242424242"
    
    print("\n" + "=" * 60)
    print("Lemon Squeezy Payment Bot - Example")
    print("=" * 60 + "\n")
    
    # Create bot
    bot = LemonSqueezyBot()
    
    try:
        # Navigate to checkout page
        print(f"Opening checkout page...")
        bot.driver.get(CHECKOUT_URL)
        
        print("\nWaiting for page to load...")
        time.sleep(3)
        
        # Fill the complete form
        print("\nFilling payment form...")
        bot.fill_complete_form(
            email="testbuyer@example.com",
            card_number=TEST_CARD,
            exp_date="1225",  # December 2025
            cvc="123",
            name="John Doe",
            country="US",
            address="123 Main Street",
            city="New York",
            postal_code="10001",
            state="New York",  # Required for US addresses
            otp_code="000000"  # Test mode OTP code
        )
        
        print("\n" + "=" * 60)
        print("✅ Form filled successfully!")
        print("=" * 60)
        print("\nWhat the bot did:")
        print("  ✓ Entered email")
        print("  ✓ Entered OTP code (000000 in test mode)")
        print("  ✓ Filled card details (test card)")
        print("  ✓ Completed billing address")
        
        # Ask if user wants to submit
        print("\n" + "=" * 60)
        print("Ready to submit payment")
        print("=" * 60)
        print("\n⚠️  This will click the Pay button and wait for redirect")
        print("📌 Using test mode - no real charges will be made")
        
        choice = input("\nSubmit the form? (y/n): ").strip().lower()
        
        if choice == 'y':
            print("\nSubmitting form...")
            success = bot.submit_form(wait_for_redirect=True, redirect_timeout=30)
            
            if success:
                print("\n🎉 Payment completed successfully!")
                print("Check the browser for the success page.")
            else:
                print("\n⚠️  Payment submission had issues.")
                print("Check the browser for any error messages.")
        else:
            print("\n✋ Submission cancelled - form filled but not submitted")
        
        input("\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to close the browser...")
    
    finally:
        bot.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LEMON SQUEEZY CHECKOUT AUTOMATION")
    print("=" * 60)
    print("\n✨ What this bot does:")
    print("   • Fills email address")
    print("   • Enters OTP code (000000 in test mode)")
    print("   • Completes card details")
    print("   • Fills billing address")
    print("\n⚠️  Test mode only - uses Stripe test card")
    print("📝 Form is filled but NOT submitted automatically")
    print("🔍 You can review everything before submitting")
    print("\n" + "=" * 60 + "\n")
    
    main()
