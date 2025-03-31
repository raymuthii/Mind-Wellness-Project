# backend/commands.py
from flask.cli import with_appcontext
from backend.extensions import db

@with_appcontext
def init_db():
    db.create_all()
    print("Database tables created successfully!")

def register_commands(app):
    app.cli.add_command(init_db, name="init-db")
