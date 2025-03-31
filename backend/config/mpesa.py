import os
from dotenv import load_dotenv

load_dotenv()

class MPESAConfig:
    """MPESA-specific configuration settings for Mind Wellness"""
    MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT', 'sandbox')
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', 'bXjGucQUBnIZo3Ho0KorIhBpC3NwlnWN1Lw3z2ALMPgWnrdC')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', 'RV0evQKG8IUnRG8lKo698jbPAB29ZfhZqWTsD32RS7LVRfflGb4DWYSALrNUvGGR')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', '')
    
    # API endpoints
    MPESA_ENDPOINTS = {
        'sandbox': {
            'base_url': 'https://sandbox.safaricom.co.ke',
            'token_url': '/oauth/v1/generate',
            'stk_push_url': '/mpesa/stkpush/v1/processrequest',
            'callback_url': os.getenv('MPESA_CALLBACK_URL', 'https://mindwellness.com/api/payments/callback')
        },
        'production': {
            'base_url': 'https://api.safaricom.co.ke',
            'token_url': '/oauth/v1/generate',
            'stk_push_url': '/mpesa/stkpush/v1/processrequest',
            'callback_url': os.getenv('MPESA_CALLBACK_URL')
        }
    }
    
    @classmethod
    def get_endpoints(cls):
        """Get the appropriate endpoints based on environment"""
        return cls.MPESA_ENDPOINTS[cls.MPESA_ENVIRONMENT]
