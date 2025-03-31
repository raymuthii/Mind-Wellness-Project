from marshmallow import fields, validate, post_load
from . import BaseSchema
from backend.models.testimonial import Testimonial
import marshmallow as ma

class TestimonialSchema(BaseSchema):
    # Name with length constraints
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    
    # Description with max length of 1000 characters
    description = fields.String(validate=validate.Length(max=1000))
    
    # Contact information
    contact_info = fields.String(validate=validate.Length(max=255))
    
    # Status field
    status = fields.String(validate=validate.OneOf(['active', 'inactive']), missing='active')
    
    # Foreign key for the provider (formerly charity)
    provider_id = fields.Integer(required=True)
    
    # Nested relationships
    provider = fields.Nested('ProviderSchema', only=('id', 'name'), dump_only=True)
    inventory_received = fields.Nested('InventorySchema', many=True, exclude=('testimonial',), dump_only=True)

    @ma.post_load
    def make_testimonial(self, data, **kwargs):
        return Testimonial(**data)
    
    # Meta class for custom error messages
    class Meta:
        error_messages = {
            'required': 'This field is required.',
            'null': 'This field cannot be null.',
            'validator_failed': 'Invalid data provided.'
        }
