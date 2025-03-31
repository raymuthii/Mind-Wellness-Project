from marshmallow import fields, validate, post_load
from . import BaseSchema
from backend.models.user import User
import marshmallow as ma

class UserSchema(BaseSchema):
    # Field for the user's name between 2 and 100 characters
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    
    # Field for the user's email, required and validated to ensure it's a properly formatted email address
    email = fields.Email(required=True)
    
    # Field for the user's password with a minimum length of 6 characters
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6))
    
    # Field for the user's role
    role = fields.String(validate=validate.OneOf(['user', 'admin', 'provider_admin']))
    
    # Boolean field indicating if the user is active, defaults to True if not provided
    is_active = fields.Boolean(missing=True)
    
    # URL field for the user's profile image
    profile_image = fields.Url(allow_none=True)
    
    # Nested fields
    # For the user's donations
    donations = fields.Nested('DonationSchema', many=True, exclude=('donor',), dump_only=True)
    
    # For the provider managed by the user (if applicable)
    managed_provider = fields.Nested('ProviderSchema', exclude=('admin',), dump_only=True)
    
    # For the user's success stories
    success_stories = fields.Nested('SuccessStorySchema', many=True, exclude=('author',), dump_only=True)

    @ma.post_load
    def make_user(self, data, **kwargs):
        return User(**data)
