from marshmallow import fields, validate, post_load
from . import BaseSchema
from ..models.success_story import SuccessStory
import marshmallow as ma

class SuccessStorySchema(BaseSchema):
    # Title with 3-200 characters
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    
    # Content
    content = fields.String(required=True)
    
    # Image URL
    image_url = fields.Url(allow_none=True)
    
    status = fields.String(validate=validate.OneOf(['draft', 'published', 'archived']))
    featured = fields.Boolean(missing=False)
    
    # Read-only fields
    view_count = fields.Integer(dump_only=True)
    likes = fields.Integer(dump_only=True)
    shares = fields.Integer(dump_only=True)
    
    # Foreign keys
    author_id = fields.Integer(required=True)
    provider_id = fields.Integer(required=True)  # Updated from charity_id
    
    # Related author and provider data
    author = fields.Nested('UserSchema', only=('id', 'name'), dump_only=True)
    provider = fields.Nested('ProviderSchema', only=('id', 'name'), dump_only=True)  # Updated from CharitySchema

    @ma.post_load
    def make_success_story(self, data, **kwargs):
        return SuccessStory(**data)
