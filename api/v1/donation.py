"""Donation routes"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import donation_bp
from models import Donation
from services import StripePaymentService

# Initialize services
stripe_service = StripePaymentService()

@donation_bp.route('/', methods=['POST'])
@jwt_required()
def create_donation():
    """Create a new donation"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate request data
        if not data or 'amount' not in data:
            return jsonify({'error': 'Amount is required'}), 400
            
        # Create Stripe checkout session
        checkout_result = stripe_service.create_checkout_session(
            amount=float(data['amount']),
            donation_id=str(current_user_id)
        )
        
        if not checkout_result['success']:
            return jsonify({
                'error': checkout_result.get('error', 'Failed to create payment session')
            }), 400
            
        return jsonify({
            'amount': data['amount'],
            'user_id': current_user_id,
            'checkout_url': checkout_result['url']
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@donation_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    signature = request.headers.get('stripe-signature')
    if not signature:
        return jsonify({'error': 'No signature provided'}), 400
        
    success, message = stripe_service.handle_webhook(
        payload=request.get_data(),
        signature=signature
    )
    
    if not success:
        return jsonify({'error': message}), 400
        
    return jsonify({
        'status': 'success',
        'message': message
    }), 200 