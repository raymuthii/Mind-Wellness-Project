import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Test amount
test_amount = 10.00  # $10.00

try:
    # Test 1: Create a checkout session
    print("Creating checkout session...")
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Test Donation',
                    'description': 'Test payment',
                },
                'unit_amount': int(test_amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:3000/success',
        cancel_url='http://localhost:3000/cancel',
    )
    print("✅ Successfully created checkout session")
    print(f"Session ID: {session.id}")
    print(f"Checkout URL: {session.url}")
    
    # Test 2: Verify the session
    print("\nVerifying session...")
    retrieved_session = stripe.checkout.Session.retrieve(session.id)
    print(f"✅ Successfully retrieved session")
    print(f"Session status: {retrieved_session.status}")
    print(f"Payment status: {retrieved_session.payment_status}")
    
except stripe.error.AuthenticationError as e:
    print(f"❌ Failed to authenticate with Stripe: {str(e)}")
except stripe.error.StripeError as e:
    print(f"❌ Stripe error: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}") 