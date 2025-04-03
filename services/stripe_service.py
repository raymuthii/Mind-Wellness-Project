import stripe
from core.stripe_config import StripeConfig

class StripePaymentService:
    def __init__(self):
        """Initialize Stripe with configuration"""
        stripe.api_key = StripeConfig.STRIPE_SECRET_KEY
        self.currency = StripeConfig.STRIPE_CURRENCY
        self.success_url = StripeConfig.STRIPE_SUCCESS_URL
        self.cancel_url = StripeConfig.STRIPE_CANCEL_URL

    def create_checkout_session(self, amount: float, donation_id: str) -> dict:
        """Create a Stripe checkout session for payment"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': self.currency,
                        'product_data': {
                            'name': 'Mind Wellness Donation',
                            'description': 'Thank you for your support!',
                        },
                        'unit_amount': int(amount * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=self.success_url,
                cancel_url=self.cancel_url,
                metadata={
                    'donation_id': donation_id,
                },
            )
            return {
                'session_id': session.id,
                'url': session.url,
                'success': True
            }
        except stripe.error.StripeError as e:
            return {
                'error': str(e),
                'success': False
            }

    def handle_webhook(self, payload: bytes, signature: str) -> tuple:
        """Handle Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, StripeConfig.STRIPE_WEBHOOK_SECRET
            )
            
            if event.type == 'checkout.session.completed':
                session = event.data.object
                donation_id = session.metadata.get('donation_id')
                return True, "Payment processed successfully"
            
            return True, "Webhook processed"
            
        except stripe.error.SignatureVerificationError:
            return False, "Invalid signature"
        except Exception as e:
            return False, str(e) 