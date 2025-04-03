"""Stripe payment service"""
import stripe
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class StripePaymentService:
    def __init__(self):
        """Initialize Stripe with configuration"""
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        if not stripe.api_key:
            logger.error("STRIPE_SECRET_KEY not found in environment variables")
            raise ValueError("STRIPE_SECRET_KEY is required")

        self.currency = os.getenv('STRIPE_CURRENCY', 'usd')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3001')
        self.success_url = os.getenv('STRIPE_SUCCESS_URL', f'{frontend_url}/payment/success')
        self.cancel_url = os.getenv('STRIPE_CANCEL_URL', f'{frontend_url}/payment/cancel')
        
        logger.info(f"Stripe service initialized with success_url: {self.success_url}, cancel_url: {self.cancel_url}")

    def create_checkout_session(self, amount: float, donation_id: str) -> dict:
        """Create a Stripe checkout session for payment"""
        try:
            logger.info(f"Creating checkout session for amount: {amount}, donation_id: {donation_id}")
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
            logger.info(f"Successfully created checkout session: {session.id}")
            return {
                'session_id': session.id,
                'url': session.url,
                'success': True
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout session: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
        except Exception as e:
            logger.error(f"Unexpected error creating checkout session: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    def handle_webhook(self, payload: bytes, signature: str) -> tuple:
        """Handle Stripe webhook events"""
        try:
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            if not webhook_secret:
                logger.error("STRIPE_WEBHOOK_SECRET not found in environment variables")
                return False, "Webhook secret not configured"

            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            logger.info(f"Processing webhook event type: {event.type}")
            
            if event.type == 'checkout.session.completed':
                session = event.data.object
                donation_id = session.metadata.get('donation_id')
                logger.info(f"Payment completed for donation_id: {donation_id}")
                return True, "Payment processed successfully"
            
            return True, "Webhook processed"
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {str(e)}")
            return False, "Invalid signature"
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return False, str(e) 