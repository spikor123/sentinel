from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    """Admin table for dashboard access."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, default="admin")
    password_hash = db.Column(db.String(128), nullable=False)

class AppUsage(db.Model):
    """Logs when an application was running."""
    id = db.Column(db.Integer, primary_key=True)
    executable_name = db.Column(db.String(255), nullable=False)
    process_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Integer, default=0)

class Blacklist(db.Model):
    """Applications that are explicitly blocked."""
    id = db.Column(db.Integer, primary_key=True)
    executable_name = db.Column(db.String(255), unique=True, nullable=False)
    friendly_name = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

class AppLimit(db.Model):
    """Time limits for specific applications."""
    id = db.Column(db.Integer, primary_key=True)
    executable_name = db.Column(db.String(255), unique=True, nullable=False)
    daily_limit_minutes = db.Column(db.Integer, default=60)

class SystemSettings(db.Model):
    """Overall system configuration."""
    id = db.Column(db.Integer, primary_key=True)
    total_screen_time_limit_minutes = db.Column(db.Integer, default=480) # 8 hours default
    lock_status = db.Column(db.Boolean, default=False)
