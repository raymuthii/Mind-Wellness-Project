import sys
from pathlib import Path

# Add the project root to Python path (ensure that the project is now renamed if applicable)
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from backend.app import create_app
from backend.extensions import db
from flask_migrate import Migrate

# Create the Mind Wellness app
app = create_app()

# Initialize Migrate for database migrations
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
