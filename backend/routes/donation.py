from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal
from models.donation import Donation
from models.user import User
from backend.models.provider import Provider  # Updated import: use Provider instead of Charity
from services.donation_service import DonationService
from ..services.payment_service import MpesaPaymentService  # Added import

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/create', methods=['POST'])
@jwt_required()
def create_donation():
    try:
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get data from request
        data = request.get_json()
        provider_id = data.get('provider_id')  # Updated key from charity_id to provider_id
        amount = data.get('amount')
        is_recurring = data.get('is_recurring', False)
        recurring_frequency = data.get('recurring_frequency')
        
        # Validate provider
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        # Create donation
        donation = DonationService.create_donation(
            user_id=user.id,
            provider_id=provider.id,  # Updated parameter name
            amount=Decimal(str(amount)),
            payment_method=Donation.PAYMENT_METHODS['MPESA'],
            is_recurring=is_recurring,
            recurring_frequency=Donation.FREQUENCIES.get(recurring_frequency.upper()) if recurring_frequency else None
        )
        
        # Complete the donation (this may vary depending on your payment flow)
        DonationService.complete_donation(donation.id)
        
        # Get updated provider total
        total = DonationService.get_provider_total(provider.id)
        return jsonify({
            'message': 'Donation successful',
            'donation': {
                'id': donation.id,
                'amount': donation.formatted_amount,
                'provider': provider.name,
                'status': donation.status
            },
            'provider_total': f"KES {total:,.2f}"
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Function to process donation via MPESA
def process_donation(user_id, provider_id, amount, phone_number):
    try:
        # Validate user
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found', 'status': 404}
        
        # Validate provider
        provider = Provider.query.get(provider_id)
        if not provider:
            return {'error': 'Provider not found', 'status': 404}
        
        # Create donation using MPESA service
        mpesa_service = MpesaPaymentService()
        donation_result = mpesa_service.initiate_payment(
            user_id=user_id,
            provider_id=provider_id,
            amount=amount,
            phone_number=phone_number
        )
        
        return donation_result
    except Exception as e:
        return {'error': str(e), 'status': 500}

@donation_bp.route('/donate', methods=['POST'])
@jwt_required()
def donate():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    result = process_donation(
        user_id=user_id,
        provider_id=data['provider_id'],  # Updated parameter name
        amount=data['amount'],
        phone_number=data['phone_number']
    )
    
    return jsonify(result), result.get('status', 200)

@donation_bp.route('/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    mpesa_service = MpesaPaymentService()
    success, message = mpesa_service.handle_callback(data)
    
    return jsonify({
        'success': success,
        'message': message
    })
