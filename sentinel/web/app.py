from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database.models import db, Admin
from database.db_manager import init_app_db
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sentinel-secure-key-123' # Should be changed in production
    
    # Initialize DB
    init_app_db(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    # Register blueprints (or simple imports)
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
