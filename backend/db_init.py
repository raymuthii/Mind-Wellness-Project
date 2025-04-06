"""Database initialization script"""
from backend import create_app, db

def init_db():
    """Initialize the database and create all tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 