"""Create and initialize the database"""
import os
from dotenv import load_dotenv
from flask import Flask
from extensions import db

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    # Create all tables
    db.create_all()
    print(f"Database tables created successfully! Using database: {app.config['SQLALCHEMY_DATABASE_URI']}") 