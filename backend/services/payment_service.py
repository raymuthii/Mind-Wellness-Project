import requests
from datetime import datetime
import base64
from database import db
from models.donation import Donation

class MpesaPaymentService:
    def __init__(self):
        self.business_shortcode = "174379"  # Your Mpesa shortcode
        self.consumer_key = "your_consumer_key"
        self.consumer_secret = "your_consumer_secret"
        self.passkey = "your_passkey"  # Used for generating password
        self.callback_url = "https://mindwellness.com/api/payments/callback"  # Updated domain
        
    def _generate_password(self):
        """Generate the M-Pesa password using shortcode and passkey"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_str.encode()).decode()
        
    def _get_access_token(self):
        """Get OAuth access token from Safaricom"""
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def initiate_payment(self, phone_number, amount, donation_id):
        """Initiate M-Pesa STK push payment"""
        access_token = self._get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self._generate_password()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": f"Donation-{donation_id}",
            "TransactionDesc": "Mental Health Donation"  # Updated description
        }
        
        try:
            response = requests.post(
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to initiate payment: {str(e)}")

    def handle_callback(self, callback_data):
        """Handle M-Pesa callback after payment"""
        try:
            result = callback_data['Body']['stkCallback']
            merchant_request_id = result['MerchantRequestID']
            checkout_request_id = result['CheckoutRequestID']
            result_code = result['ResultCode']
            
            if result_code == 0:  # Successful payment
                # Extract payment details
                payment_data = result['CallbackMetadata']['Item']
                amount = next(item['Value'] for item in payment_data if item['Name'] == 'Amount')
                mpesa_receipt = next(item['Value'] for item in payment_data if item['Name'] == 'MpesaReceiptNumber')
                phone = next(item['Value'] for item in payment_data if item['Name'] == 'PhoneNumber')
                
                # Update donation record: extract donation ID from the ResultDesc reference
                donation_ref = result['ResultDesc'].split('-')[1]
                donation = Donation.query.get(donation_ref)
                if donation:
                    donation.status = 'completed'
                    donation.transaction_id = mpesa_receipt
                    db.session.commit()
                    return True, "Payment processed successfully"
            
            return False, f"Payment failed with code: {result_code}"
            
        except Exception as e:
            return False, f"Error processing callback: {str(e)}"

# Usage example in your donation route
def process_donation(user_id, provider_id, amount, phone_number):
    try:
        # Create pending donation record (note: provider_id used instead of charity_id)
        donation = Donation(
            donor_id=user_id,
            provider_id=provider_id,
            amount=amount,
            status='pending',
            payment_method='mpesa'
        )
        db.session.add(donation)
        db.session.commit()
        
        # Initialize payment
        mpesa_service = MpesaPaymentService()
        payment_response = mpesa_service.initiate_payment(
            phone_number=phone_number,
            amount=amount,
            donation_id=donation.id
        )
        
        return {
            'success': True,
            'message': 'Payment initiated',
            'donation_id': donation.id,
            'checkout_request_id': payment_response['CheckoutRequestID']
        }
        
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': str(e)
        }
