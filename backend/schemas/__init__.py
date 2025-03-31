from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from datetime import datetime

class BaseSchema(Schema):
    """Base schema for Mind Wellness models with common fields and validations."""
    id = fields.Integer(dump_only=True)
    
    # Automatically dump the created timestamp using the current UTC time
    created_at = fields.DateTime(dump_only=True, missing=datetime.utcnow)
    
    # Automatically dump the updated timestamp using the current UTC time
    updated_at = fields.DateTime(dump_only=True, missing=datetime.utcnow)
    
    @validates('created_at')
    def validate_created_at(self, value):
        if value and not isinstance(value, datetime):
            raise ValidationError('Invalid datetime format for created_at.')
    
    @validates('updated_at')
    def validate_updated_at(self, value):
        if value and not isinstance(value, datetime):
            raise ValidationError('Invalid datetime format for updated_at.')
    
    @post_load
    def process_data(self, data, **kwargs):
        # Additional processing after data load can be added here if needed
        return data

    class Meta:
        error_messages = {
            'required': 'This field is required.',
            'null': 'This field cannot be null.',
            'validator_failed': 'Invalid data provided.'
        }
