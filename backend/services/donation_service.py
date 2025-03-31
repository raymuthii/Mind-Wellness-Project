from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from enum import Enum
from contextlib import contextmanager
from app import db
from models.donation import Donation
from models.user import User
from backend.models.provider import Provider  # Updated: Provider instead of Charity
import logging
from database import db  # Ensure this import aligns with your project structure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom Exceptions
class DonationError(Exception):
    """Base exception for donation-related errors"""
    pass

class InvalidDonationError(DonationError):
    """Raised when donation parameters are invalid"""
    pass

class EntityNotFoundError(DonationError):
    """Raised when referenced entities are not found"""
    pass

# Enums
class PaymentMethod(Enum):
    MPESA = "MPESA"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"

    @classmethod
    def validate(cls, payment_method: str) -> str:
        try:
            return cls[payment_method.upper()].value
        except KeyError:
            raise InvalidDonationError(
                f"Invalid payment method. Supported methods: {', '.join(cls._member_names_)}"
            )

class RecurringFrequency(Enum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"

    @classmethod
    def validate(cls, frequency: str) -> str:
        try:
            return cls[frequency.upper()].value
        except KeyError:
            raise InvalidDonationError(
                f"Invalid recurring frequency. Supported frequencies: {', '.join(cls._member_names_)}"
            )

@contextmanager
def transaction_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise

class DonationService:
    # Constants
    MIN_DONATION_AMOUNT = Decimal('1.00')
    MAX_DONATION_AMOUNT = Decimal('1000000.00')

    @staticmethod
    def create_donation(
        user_id: int,
        provider_id: int,  # Updated parameter: provider_id instead of charity_id
        amount: Decimal,
        payment_method: str,
        is_recurring: bool = False,
        recurring_frequency: Optional[str] = None
    ) -> Donation:
        """
        Create a new donation with improved error handling.
        
        Args:
            user_id: ID of the donor.
            provider_id: ID of the provider.
            amount: Donation amount.
            payment_method: Payment method (e.g., MPESA, CARD, BANK_TRANSFER).
            is_recurring: Whether this is a recurring donation.
            recurring_frequency: Frequency of recurring donations.
            
        Returns:
            Donation object.
            
        Raises:
            InvalidDonationError: If donation parameters are invalid.
            EntityNotFoundError: If user or provider not found.
            DonationError: For other donation-related errors.
        """
        # Validate amount
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        if amount < DonationService.MIN_DONATION_AMOUNT:
            raise InvalidDonationError(f"Donation amount must be at least {DonationService.MIN_DONATION_AMOUNT}")
        
        if amount > DonationService.MAX_DONATION_AMOUNT:
            raise InvalidDonationError(f"Donation amount cannot exceed {DonationService.MAX_DONATION_AMOUNT}")
        
        # Validate payment method
        validated_payment_method = PaymentMethod.validate(payment_method)
        
        # Validate recurring donation parameters
        if is_recurring:
            if not recurring_frequency:
                raise InvalidDonationError("Recurring frequency is required for recurring donations")
            validated_frequency = RecurringFrequency.validate(recurring_frequency)
        else:
            validated_frequency = None
        
        # Verify entities
        user = User.query.get(user_id)
        if not user:
            raise EntityNotFoundError(f"User with ID {user_id} not found")
            
        provider = Provider.query.get(provider_id)  # Updated: provider instead of charity
        if not provider:
            raise EntityNotFoundError(f"Provider with ID {provider_id} not found")
        
        with transaction_scope():
            try:
                donation = Donation(
                    donor_id=user_id,
                    provider_id=provider_id,  # Updated: provider_id
                    amount=amount,
                    payment_method=validated_payment_method,
                    is_recurring=is_recurring,
                    recurring_frequency=validated_frequency,
                    status='pending',
                    created_at=datetime.utcnow()
                )
                
                db.session.add(donation)
                logger.info(
                    f"Created donation of {amount} for provider {provider_id} "
                    f"by user {user_id}"
                )
                return donation
                
            except Exception as e:
                logger.error(f"Failed to create donation: {str(e)}")
                raise DonationError(f"Failed to create donation: {str(e)}")

    @staticmethod
    def get_user_donations(user_id: int) -> List[Donation]:
        """Get all donations for a specific user"""
        if not User.query.get(user_id):
            raise EntityNotFoundError(f"User with ID {user_id} not found")
            
        try:
            donations = Donation.query.filter_by(donor_id=user_id).order_by(
                Donation.created_at.desc()
            ).all()
            
            logger.info(f"Retrieved {len(donations)} donations for user {user_id}")
            return donations
            
        except Exception as e:
            logger.error(f"Error fetching donations for user {user_id}: {str(e)}")
            raise DonationError(f"Failed to fetch user donations: {str(e)}")

    @staticmethod
    def get_donation(donation_id: int) -> Optional[Donation]:
        """Get a specific donation by ID"""
        try:
            donation = Donation.query.get(donation_id)
            if donation:
                logger.info(f"Retrieved donation {donation_id}")
            else:
                logger.info(f"No donation found with ID {donation_id}")
            return donation
            
        except Exception as e:
            logger.error(f"Error fetching donation {donation_id}: {str(e)}")
            raise DonationError(f"Failed to fetch donation: {str(e)}")

    @staticmethod
    def get_donations_by_provider(provider_id: int) -> List[Donation]:
        """Get all completed donations for a specific provider"""
        if not Provider.query.get(provider_id):
            raise EntityNotFoundError(f"Provider with ID {provider_id} not found")
            
        try:
            donations = Donation.query.filter_by(
                provider_id=provider_id,
                status='completed'
            ).order_by(Donation.created_at.desc()).all()
            
            logger.info(f"Retrieved {len(donations)} donations for provider {provider_id}")
            return donations
            
        except Exception as e:
            logger.error(f"Error fetching donations for provider {provider_id}: {str(e)}")
            raise DonationError(f"Failed to fetch provider donations: {str(e)}")

    @staticmethod
    def complete_donation(donation_id: int) -> Donation:
        """Complete a pending donation"""
        with transaction_scope():
            try:
                donation = Donation.query.get(donation_id)
                if not donation:
                    raise EntityNotFoundError(f"Donation with ID {donation_id} not found")
                    
                if donation.status == 'completed':
                    raise InvalidDonationError("Donation is already completed")
                    
                donation.status = 'completed'
                donation.completed_at = datetime.utcnow()
                
                logger.info(f"Completed donation {donation_id}")
                return donation
                
            except Exception as e:
                logger.error(f"Failed to complete donation: {str(e)}")
                raise DonationError(f"Failed to complete donation: {str(e)}")

    @staticmethod
    def cancel_donation(donation_id: int) -> Donation:
        """Cancel a pending donation"""
        with transaction_scope():
            try:
                donation = Donation.query.get(donation_id)
                if not donation:
                    raise EntityNotFoundError(f"Donation with ID {donation_id} not found")
                    
                if donation.status != 'pending':
                    raise InvalidDonationError(f"Cannot cancel donation with status: {donation.status}")
                    
                donation.status = 'cancelled'
                donation.cancelled_at = datetime.utcnow()
                
                logger.info(f"Cancelled donation {donation_id}")
                return donation
                
            except Exception as e:
                logger.error(f"Failed to cancel donation: {str(e)}")
                raise DonationError(f"Failed to cancel donation: {str(e)}")

    @staticmethod
    def get_provider_total(provider_id: int) -> Decimal:
        """Get total completed donations for a provider"""
        if not Provider.query.get(provider_id):
            raise EntityNotFoundError(f"Provider with ID {provider_id} not found")
            
        try:
            total = db.session.query(
                db.func.sum(Donation.amount)
            ).filter(
                Donation.provider_id == provider_id,
                Donation.status == 'completed'
            ).scalar()
            
            return total or Decimal('0.0')
            
        except Exception as e:
            logger.error(f"Error calculating provider total: {str(e)}")
            raise DonationError(f"Failed to calculate provider total: {str(e)}")
