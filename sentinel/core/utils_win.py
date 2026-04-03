import ctypes
import win32api
import win32con
import win32gui
# from plyer import notification # A cleaner wrapper if we add it to requirements, or use native

def show_block_message(app_name):
    """Native Windows Message Box to notify the user of blocking."""
    message = f"Access to '{app_name}' has been blocked by Sentinel Parental Control."
    title = "Sentinel: Application Blocked"
    # MB_OK | MB_ICONSTOP
    win32api.MessageBox(0, message, title, win32con.MB_OK | win32con.MB_ICONSTOP)

def lock_windows_session():
    """Immediately locks the current Windows user session."""
    ctypes.windll.user32.LockWorkStation()

def notify_user(title, message):
    """Desktop notification for warnings."""
    # Since we didn't add 'plyer' to requirements, we can use win32api or simplified ctypes
    # For now, let's just use the message box for high impact or simple logging
    pass
