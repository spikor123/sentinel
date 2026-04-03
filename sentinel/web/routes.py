from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from database.models import db, Admin, AppUsage, Blacklist, SystemSettings
import bcrypt
from sqlalchemy import func
from datetime import datetime, date, timedelta

bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin.password_hash.encode('utf-8')):
            login_user(admin)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

from pyngrok import ngrok

@bp.route('/')
@login_required
def dashboard():
    today = date.today()
    
    # Check for active ngrok tunnel (Remote Access)
    public_url = None
    try:
        tunnels = ngrok.get_tunnels()
        if tunnels:
            public_url = tunnels[0].public_url
    except:
        pass

    # 1. Dashboard summary stats
    # BUG FIX: Use max() instead of sum() to avoid multiplier effect in 'Total Screen Time'
    total_duration = db.session.query(func.max(AppUsage.duration_seconds))\
        .filter(func.date(AppUsage.start_time) == today).scalar() or 0
    total_hours = round(total_duration / 3600, 1)
    
    # 2. Top 5 Applications for Chart.js
    top_apps_data = db.session.query(
        AppUsage.executable_name, 
        func.sum(AppUsage.duration_seconds).label('total')
    ).filter(func.date(AppUsage.start_time) == today)\
     .group_by(AppUsage.executable_name)\
     .order_by(func.sum(AppUsage.duration_seconds).desc()).limit(5).all()
    
    # Format labels and values for Chart.js
    labels = [row[0] for row in top_apps_data]
    values = [round(row[1] / 60, 1) for row in top_apps_data] # Minutes
    
    # 3. Overall Limit Warning
    settings = SystemSettings.query.first()
    limit_reached = (total_duration >= (settings.total_screen_time_limit_minutes * 60))
    
    return render_template('dashboard.html', 
                          total_hours=total_hours,
                          labels=labels,
                          values=values,
                          limit_reached=limit_reached,
                          settings=settings,
                          public_url=public_url)

@bp.route('/blacklist', methods=['GET', 'POST'])
@login_required
def blacklist():
    if request.method == 'POST':
        new_app = request.form.get('executable_name').strip()
        friendly_n = request.form.get('friendly_name', new_app)
        if new_app:
            # Check if already exists
            if not Blacklist.query.filter_by(executable_name=new_app).first():
                entry = Blacklist(executable_name=new_app, friendly_name=friendly_n)
                db.session.add(entry)
                db.session.commit()
                flash(f"'{new_app}' added to blacklist.", "success")
        return redirect(url_for('main.blacklist'))
    
    # Fetch all currently known app names to suggest for easy blacklisting
    blacklist_names = [item.executable_name.lower() for item in Blacklist.query.all()]
    
    # Suggest apps seen today that aren't blacklisted yet
    query = db.session.query(AppUsage.executable_name, func.max(AppUsage.start_time))\
        .group_by(AppUsage.executable_name)\
        .order_by(func.max(AppUsage.start_time).desc())
    
    # SQLite fails if an empty list is passed to .in_()
    if blacklist_names:
        query = query.filter(func.not_(func.lower(AppUsage.executable_name).in_(blacklist_names)))
    
    suggestions = query.limit(10).all()
    
    items = Blacklist.query.all()
    return render_template('blacklist.html', items=items, suggestions=suggestions)

import time
from sqlalchemy.exc import OperationalError

@bp.route('/blacklist/remove/<int:id>')
@login_required
def remove_blacklist(id):
    for attempt in range(5):
        try:
            entry = Blacklist.query.get_or_404(id)
            name = entry.executable_name
            db.session.delete(entry)
            db.session.commit()
            flash(f"'{name}' removed from blacklist.", "info")
            return redirect(url_for('main.blacklist'))
        except OperationalError as e:
            if "locked" in str(e).lower() and attempt < 4:
                db.session.rollback()
                time.sleep(0.5) # Wait for monitor to finish its tick
                continue
            raise
    return redirect(url_for('main.blacklist'))

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = SystemSettings.query.first()
    if request.method == 'POST':
        limit = request.form.get('limit')
        if limit and limit.isdigit():
            settings.total_screen_time_limit_minutes = int(limit)
            db.session.commit()
            flash("System settings updated.", "success")
    return render_template('settings.html', settings=settings)

@bp.route('/logs')
@login_required
def activity_logs():
    # Show last 50 usage events
    logs = AppUsage.query.order_by(AppUsage.start_time.desc()).limit(50).all()
    return render_template('logs.html', logs=logs)
