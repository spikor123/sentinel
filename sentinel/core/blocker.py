import psutil
from database.models import db, Blacklist, SystemSettings
from .utils_win import show_block_message
import logging

class SentinelBlocker:
    def __init__(self, db_scoped_session):
        self.db = db_scoped_session
        self.logger = logging.getLogger("SentinelBlocker")
        self.cached_blacklist = []

    def refresh_blacklist_cache(self):
        """Fetch and cache active blocked names for the current scan cycle."""
        # Using .lower() here for consistent matching
        self.cached_blacklist = [item.executable_name.lower() for item in Blacklist.query.filter_by(is_active=True).all()]

    def check_and_enforce(self, pinfo):
        """
        Check if a given process info belongs to the cached blacklist.
        """
        try:
            name = pinfo.info['name'].lower()
            pid = pinfo.info['pid']
            
            # Simple inclusion check (supports .exe and non-.exe names)
            is_blocked = False
            for blocked_n in self.cached_blacklist:
                if name == blocked_n or (name.endswith('.exe') and name[:-4] == blocked_n):
                    is_blocked = True
                    break
            
            if is_blocked:
                # Kill the process
                proc = psutil.Process(pid)
                proc.terminate()
                self.logger.warning(f"BLOCKED: Terminated unauthorized process '{name}' (PID: {pid}).")
                
                # Show popup 
                show_block_message(name)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return False
