import os
from dotenv import load_dotenv

load_dotenv()

class StripeConfig:
    """Stripe-specific configuration settings for Mind Wellness"""
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    
    # Test mode
    STRIPE_TEST_MODE = os.getenv('STRIPE_TEST_MODE', 'true').lower() == 'true'
    
    # Currency
    STRIPE_CURRENCY = os.getenv('STRIPE_CURRENCY', 'usd')
    
    # Success and cancel URLs for checkout
    STRIPE_SUCCESS_URL = os.getenv('STRIPE_SUCCESS_URL', 'http://localhost:3000/payment/success')
    STRIPE_CANCEL_URL = os.getenv('STRIPE_CANCEL_URL', 'http://localhost:3000/payment/cancel')
    
    @classmethod
    def get_stripe_keys(cls):
        """Get the appropriate Stripe keys based on test mode"""
        return {
            'public_key': cls.STRIPE_PUBLIC_KEY,
            'secret_key': cls.STRIPE_SECRET_KEY,
            'webhook_secret': cls.STRIPE_WEBHOOK_SECRET
        } 