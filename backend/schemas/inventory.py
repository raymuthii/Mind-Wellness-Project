from marshmallow import fields, validate, post_load
from . import BaseSchema
from backend.models.inventory import Inventory
import marshmallow as ma

class InventorySchema(BaseSchema):
    # Item name with length 2-100
    item_name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    
    # Item description
    description = fields.String()
    
    # Quantity, required and must not be negative
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    
    # Status
    status = fields.String(validate=validate.OneOf(['in_stock', 'allocated', 'distributed']))
    
    # Foreign keys
    provider_id = fields.Integer(required=True)  # Renamed from charity_id
    testimonial_id = fields.Integer()             # Renamed from beneficiary_id
    
    # Related provider and testimonial data, read-only
    provider = fields.Nested('ProviderSchema', only=('id', 'name'), dump_only=True)
    testimonial = fields.Nested('TestimonialSchema', only=('id', 'name'), dump_only=True)

    @ma.post_load
    def make_inventory(self, data, **kwargs):
        return Inventory(**data)
