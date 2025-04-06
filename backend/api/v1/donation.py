"""Donation endpoints"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

from backend.models import User, Donation, db
from backend.services.stripe_service import StripePaymentService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
stripe_service = StripePaymentService()

def init_donation_routes(bp):
    @bp.route('/donation/', methods=['POST'])
    @jwt_required()
    def create_donation():
        """Create a new donation"""
        try:
            data = request.get_json()
            current_user_email = get_jwt_identity()
            
            # Get user from database
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                logger.error(f"User not found for email: {current_user_email}")
                return jsonify({'error': 'User not found'}), 404
            
            # Validate request data
            if not data or 'amount' not in data:
                logger.error("Missing amount in donation request")
                return jsonify({'error': 'Amount is required'}), 400
            
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError as e:
                logger.error(f"Invalid amount format: {data.get('amount')}")
                return jsonify({'error': 'Invalid amount format. Amount must be a positive number'}), 400
                
            # Create Stripe checkout session
            checkout_result = stripe_service.create_checkout_session(
                amount=amount,
                donation_id=str(user.id)
            )
            
            if not checkout_result['success']:
                logger.error(f"Failed to create Stripe session: {checkout_result.get('error')}")
                return jsonify({
                    'error': checkout_result.get('error', 'Failed to create payment session')
                }), 400
            
            # Create donation record
            donation = Donation(
                amount=amount,
                user_id=user.id,
                status='pending',
                transaction_id=checkout_result['session_id']
            )
            
            try:
                db.session.add(donation)
                db.session.commit()
                logger.info(f"Created donation record for user {user.id} with amount {amount}")
            except Exception as e:
                logger.error(f"Database error creating donation: {str(e)}")
                db.session.rollback()
                # Continue anyway since we have the checkout URL
                
            return jsonify({
                'amount': amount,
                'user_id': user.id,
                'checkout_url': checkout_result['url']
            }), 200
            
        except Exception as e:
            logger.error(f"Unexpected error in create_donation: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @bp.route('/donation/webhook', methods=['POST'])
    def stripe_webhook():
        """Handle Stripe webhook events"""
        signature = request.headers.get('stripe-signature')
        if not signature:
            logger.error("Missing Stripe signature in webhook request")
            return jsonify({'error': 'No signature provided'}), 400
            
        success, message = stripe_service.handle_webhook(
            payload=request.get_data(),
            signature=signature
        )
        
        if not success:
            logger.error(f"Webhook processing failed: {message}")
            return jsonify({'error': message}), 400
            
        logger.info("Successfully processed webhook")
        return jsonify({
            'status': 'success',
            'message': message
        }), 200

    @bp.route('/donation/', methods=['GET'])
    @jwt_required()
    def get_donations():
        """Get all donations for the current user"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            
            if not user:
                logger.error(f"User not found for email: {current_user_email}")
                return jsonify({'error': 'User not found'}), 404
            
            donations = Donation.query.filter_by(user_id=user.id).all()
            return jsonify({
                'donations': [{
                    'id': d.id,
                    'amount': d.amount,
                    'status': d.status,
                    'transaction_id': d.transaction_id
                } for d in donations]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching donations: {str(e)}")
            return jsonify({'error': 'Failed to fetch donations'}), 500

# Initialize routes with the donation blueprint
donation_bp = Blueprint('donation', __name__)
init_donation_routes(donation_bp) 