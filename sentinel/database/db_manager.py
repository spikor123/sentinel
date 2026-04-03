from flask import Flask
from .models import db, Admin, Blacklist, SystemSettings
from sqlalchemy import text
import bcrypt
import os

DB_NAME = "sentinel.db"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_NAME)

def init_app_db(app):
    """Initializes the database within the Flask context."""
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {"timeout": 30}
    }
    db.init_app(app)
    
    # Enable WAL mode for better concurrency in SQLite
    with app.app_context():
        db.create_all()
        # Set WAL mode
        db.session.execute(text("PRAGMA journal_mode=WAL"))
        db.session.commit()
        # Seed default admin if missing
        if not Admin.query.filter_by(username="admin").first():
            hashed_pwd = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_admin = Admin(username="admin", password_hash=hashed_pwd)
            db.session.add(new_admin)
            
        # Seed default system settings
        if not SystemSettings.query.first():
            default_settings = SystemSettings()
            db.session.add(default_settings)
            
        db.session.commit()
    return db

def get_db_path():
    return DB_PATH
