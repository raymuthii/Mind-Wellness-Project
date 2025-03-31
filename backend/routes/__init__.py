from flask import Blueprint

# Create blueprints for Mind Wellness platform
auth_bp = Blueprint('auth', __name__)
provider_bp = Blueprint('provider', __name__)
donation_bp = Blueprint('donation', __name__)
success_story_bp = Blueprint('success_story', __name__)
user_bp = Blueprint('user', __name__)
provider_admin_bp = Blueprint('provider_admin', __name__)
admin_bp = Blueprint('admin', __name__)

# Import routes after blueprint creation to avoid circular imports
from backend.routes import auth, provider, donation, success_story, user, provider_admin, admin
