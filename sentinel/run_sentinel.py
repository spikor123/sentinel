import threading
import sys
import os
import time

# Ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.monitor import SentinelMonitor
from web.app import create_app

from pyngrok import ngrok

def start_monitoring():
    monitor = SentinelMonitor()
    monitor.monitor_loop()

if __name__ == "__main__":
    print("-" * 40)
    print("      SENTINEL PARENTAL CONTROL      ")
    print("-" * 40)
    
    # 1. OPTIONAL REMOTE ACCESS (NGROK)
    public_url = None
    if "--remote" in sys.argv:
        print("[*] Establishing Secure Tunnel (ngrok)...")
        try:
            # Ngrok requires your auth token: ngrok config add-authtoken <YOUR_TOKEN>
            tunnel = ngrok.connect(5000)
            public_url = tunnel.public_url
            print(f"[!] REMOTE ACCESS LIVE at: {public_url}")
        except Exception as e:
            print(f"[!] Warning: Remote tunnel failed. {e}")

    print("[*] Starting Background Monitor...")
    
    # Start monitor in a background thread
    monitor_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitor_thread.start()
    
    print("[+] Monitor Service: Running")
    
    # Create and start the Flask web dashboard
    print("[*] Starting Parental Dashboard UI...")
    app = create_app()
    
    # host='0.0.0.0' allows access from other devices on the same local network
    app.run(host='0.0.0.0', port=5000, debug=True)
