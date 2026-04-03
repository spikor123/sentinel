import psutil
import time
from datetime import datetime, date
from sqlalchemy import func
from flask import Flask
from database.models import db, AppUsage, Blacklist, SystemSettings
from database.db_manager import init_app_db
from .blocker import SentinelBlocker
from .utils_win import lock_windows_session
import logging

class SentinelMonitor:
    def __init__(self):
        # Create a mock app context for DB access outside the main web thread
        self.app = Flask(__name__)
        self.db = init_app_db(self.app)
        self.blocker = SentinelBlocker(self.db)
        
        # Track active processes locally (pid -> AppUsage model ID)
        self.active_processes = {}
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger("SentinelMonitor")

    def _check_screen_time_limit(self, current_time):
        """Monitor total screen time correctly today."""
        today = date.today()
        # BUG FIX: SUM(duration_seconds) leads to a massive multiplier effect 
        # (e.g., 200 processes for 1 hour = 200 hours of 'screen time').
        # We instead calculate 'System Active Time' by finding the maximum duration 
        # any SINGLE user process has been running today.
        total_today_seconds = db.session.query(func.max(AppUsage.duration_seconds))\
            .filter(func.date(AppUsage.start_time) == today).scalar() or 0
        
        settings = SystemSettings.query.first()
        if settings and settings.total_screen_time_limit_minutes:
            limit_seconds = settings.total_screen_time_limit_minutes * 60
            if total_today_seconds >= limit_seconds:
                # We could store state, but the monitor loop runs on a 5s sync. 
                # This ensures lockout persists if they try to log back in while over limit.
                self.logger.critical(f"OVER LIMIT: Total daily screen time ({int(total_today_seconds/60)} min) exceeded. Locking workstation.")
                lock_windows_session()

    def monitor_loop(self):
        """Infinite loop to scan, log, and enforce policies."""
        self.logger.info("Sentinel Background Monitoring & Enforcement started.")
        tick_count = 0
        while True:
            try:
                # 1. PRE-SCAN: Record current processes outside DB context to keep transaction short
                scanned_data = []
                for proc in psutil.process_iter(['pid', 'name', 'username']):
                    try:
                        pinfo = proc.info
                        uname = pinfo['username']
                        if not uname or any(sys_id in (uname or "").upper() for sys_id in ["SYSTEM", "LOCAL SERVICE", "NETWORK SERVICE"]):
                            continue
                        scanned_data.append(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                # 2. DB UPDATE: Perform database operations
                with self.app.app_context():
                    current_time = datetime.utcnow()
                    active_pids_this_scan = set()
                    
                    # Refresh blacklist cache (Needed every tick for blocking)
                    self.blocker.refresh_blacklist_cache()
                    
                    # A. Quick Block Enforcement (Every 5s)
                    for proc in scanned_data:
                        if self.blocker.check_and_enforce(proc):
                            continue
                        active_pids_this_scan.add(proc.info['pid'])

                    # B. Usage History Logging (Every 30s to reduce DB contention)
                    tick_count += 1
                    if tick_count >= 6: # 6 ticks * 5 seconds = 30 seconds
                        tick_count = 0
                        self.logger.info("Updating usage logs in database...")
                        
                        # Check Screen Time
                        self._check_screen_time_limit(current_time)
                        
                        for proc in scanned_data:
                            pid = proc.info['pid']
                            if pid not in active_pids_this_scan: continue # Blocked apps skip usage
                            
                            if pid not in self.active_processes:
                                new_log = AppUsage(
                                    executable_name=proc.info['name'],
                                    process_name=proc.info['name'],
                                    username=proc.info['username'] or "Unknown",
                                    start_time=current_time,
                                    end_time=current_time,
                                    duration_seconds=0
                                )
                                db.session.add(new_log)
                                db.session.flush()
                                self.active_processes[pid] = new_log.id
                            else:
                                log_entry = AppUsage.query.get(self.active_processes[pid])
                                if log_entry:
                                    log_entry.end_time = current_time
                                    log_entry.duration_seconds = int((current_time - log_entry.start_time).total_seconds())

                        # Cleanup Terminated
                        terminated_pids = set(self.active_processes.keys()) - active_pids_this_scan
                        for pid in terminated_pids:
                            del self.active_processes[pid]

                    db.session.commit()
                    db.session.remove()
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}", exc_info=True)
            
            time.sleep(5)

if __name__ == "__main__":
    monitor = SentinelMonitor()
    monitor.monitor_loop()
