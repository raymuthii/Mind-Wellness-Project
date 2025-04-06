"""Models package initialization"""
from backend.extensions import db

# Import models after db creation to avoid circular imports
from backend.models.user import User
from backend.models.donation import Donation
from backend.models.testimonial import Testimonial
from backend.models.success_story import SuccessStory
from backend.models.appointment import Appointment

# Make models available at package level
__all__ = [
    "User",
    "Donation",
    "Testimonial",
    "SuccessStory",
    "Appointment"
] 