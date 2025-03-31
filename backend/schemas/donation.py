from marshmallow import fields, validate, post_load
from . import BaseSchema
from ..models.donation import Donation
import marshmallow as ma

class DonationSchema(BaseSchema):
    # Amount, decimal with 2 decimal places
    amount = fields.Decimal(required=True, places=2, as_string=True, validate=validate.Range(min=0.01))
    
    # Currency
    currency = fields.String(required=True, validate=validate.Length(equal=3))
    
    # Status with predefined choices and default 'pending'
    status = fields.String(validate=validate.OneOf(['pending', 'completed', 'failed']), missing='pending')
    
    # Transaction
    transaction_id = fields.String(validate=validate.Length(max=255))
    
    # Anonymous flag, defaults to False
    is_anonymous = fields.Boolean(missing=False)
    
    # Recurring flag, defaults to False
    is_recurring = fields.Boolean(missing=False)
    
    # Recurring frequency
    recurring_frequency = fields.String(validate=validate.OneOf(['monthly', 'quarterly', 'yearly']), missing=None)
    
    # Foreign keys
    donor_id = fields.Integer(required=True)
    charity_id = fields.Integer(required=True)
    
    # Nested relationships
    donor = fields.Nested('UserSchema', only=('id', 'name'), dump_only=True)
    charity = fields.Nested('CharitySchema', only=('id', 'name'), dump_only=True)

    @ma.post_load
    def make_donation(self, data, **kwargs):
        return Donation(**data)
    
    # Meta class for custom error messages
    class Meta:
        error_messages = {
            'required': 'This field is required.',
            'null': 'This field cannot be null.',
            'validator_failed': 'Invalid data provided.',
            'range': 'Value must be positive and greater than zero.'
        }
