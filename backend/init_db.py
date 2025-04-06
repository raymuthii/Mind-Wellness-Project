"""Initialize database and create tables"""
import os
import sys
from pathlib import Path

# Add the parent directory to Python path
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from backend import create_app
from backend.extensions import db

def init_db():
    """Initialize the database and create all tables"""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db() 