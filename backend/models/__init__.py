from backend.extensions import db
from backend.models.user import User
from backend.models.testimonial import Testimonial
from backend.models.success_story import SuccessStory

# Ensure all models are imported before migrations run
__all__ = ["User", "Testimonial", "SuccessStory"]
