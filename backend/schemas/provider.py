from marshmallow import fields, validate, post_load
from . import BaseSchema
from backend.models.provider import Provider
import marshmallow as ma

class ProviderSchema(BaseSchema):
    # Required name with length constraints
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    
    # Required description with max length of 1000 characters
    description = fields.String(required=True, validate=validate.Length(max=1000))
    
    # Mission statement
    mission = fields.String(validate=validate.Length(max=1000))
    
    # URLs for logo and cover images
    logo_url = fields.Url(allow_none=True, missing=None)
    cover_image = fields.Url(allow_none=True, missing=None)
    
    # Contact information
    email = fields.Email(required=True)
    phone_number = fields.String(validate=validate.Length(max=20))
    address = fields.String()
    
    # Account-related fields
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6))
    
    # Category, optional
    category = fields.String()
    
    # Status field with default 'pending' and predefined choices
    status = fields.String(validate=validate.OneOf(['pending', 'active', 'inactive']), missing='pending')
    
    # Featured flag, defaults to False
    featured = fields.Boolean(missing=False)
    
    # Foreign key for the admin
    admin_id = fields.Integer()
    
    # Nested relationships, read-only
    admin = fields.Nested('UserSchema', only=('id', 'name', 'email'), dump_only=True)
    donations = fields.Nested('DonationSchema', many=True, exclude=('provider',), dump_only=True)
    testimonials = fields.Nested('TestimonialSchema', many=True, exclude=('provider',), dump_only=True)
    success_stories = fields.Nested('SuccessStorySchema', many=True, exclude=('provider',), dump_only=True)
    inventory_items = fields.Nested('InventorySchema', many=True, exclude=('provider',), dump_only=True)

    @ma.post_load
    def make_provider(self, data, **kwargs):
        return Provider(**data)
    
    class Meta:
        error_messages = {
            'required': 'This field is required.',
            'null': 'This field cannot be null.',
            'validator_failed': 'Invalid data provided.'
        }
