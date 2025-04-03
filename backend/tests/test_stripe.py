import unittest
import stripe
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.stripe_config import StripeConfig
from services.stripe_service import StripePaymentService

class TestStripeIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test configuration"""
        self.stripe_service = StripePaymentService()
        self.test_amount = 10.00  # $10.00
        self.test_donation_id = "test_donation_123"
        
    def test_create_checkout_session(self):
        """Test if we can create a Stripe checkout session"""
        result = self.stripe_service.create_checkout_session(
            amount=self.test_amount,
            donation_id=self.test_donation_id
        )
        
        # Assert
        self.assertTrue(result['success'])
        self.assertIn('session_id', result)
        self.assertIn('url', result)
        
    def test_webhook_handling(self):
        """Test webhook handling with a mock event"""
        # Create a mock event
        mock_event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'payment_intent': 'pi_test_123',
                    'metadata': {
                        'donation_id': self.test_donation_id
                    }
                }
            }
        }
        
        # Create a mock signature
        mock_signature = 'mock_signature'
        
        # Create a mock payload
        mock_payload = str(mock_event).encode()
        
        # Test webhook handling
        success, message = self.stripe_service.handle_webhook(mock_payload, mock_signature)
        
        # Assert
        self.assertTrue(success)
        self.assertIn('success', message.lower())

if __name__ == '__main__':
    unittest.main() 