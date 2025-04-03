"""Models package"""
from extensions import db

# Import models after db creation to avoid circular imports
from .user import User
from .donation import Donation
from .testimonial import Testimonial
from .success_story import SuccessStory
from .appointment import Appointment

# Make models available at package level
__all__ = [
    "db",  # Export db instance
    "User",
    "Donation",
    "Testimonial",
    "SuccessStory",
    "Appointment"
] 