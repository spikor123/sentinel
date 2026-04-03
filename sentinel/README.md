# Sentinel | OS-Based Parental Control & Monitoring System

Sentinel is a lightweight, reliable Windows-based parental control tool designed to monitor application usage, enforce screen time limits, and provide a secure remote dashboard for parents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Key Features
- **Background Monitoring**: Silent tracking of all running applications with usage duration.
- **Application Blocking**: Instant termination of blacklisted executables.
- **Screen Time Management**: Automatically locks the Windows session once the daily limit is reached.
- **Visual Dashboard**: Real-time charts (Chart.js) and activity logs accessible via any browser on the local network.
- **Secure Access**: Session-based authentication with hashed passwords.

## 🛠️ Technical Stack
- **Backend**: Python 3.11+ (Flask)
- **Database**: SQLite (SQLAlchemy 2.0)
- **Concurrency**: WAL Mode + Threading
- **Frontend**: Bootstrap 5, Chart.js

---

## 📂 Project Structure
```bash
sentinel/
├── core/             # Monitoring and enforcement engine
├── web/              # Flask application and UI templates
├── database/         # Database models and initialization
├── assets/           # Dashboard visuals and icons
├── scripts/          # Helper utilities
└── run_sentinel.py   # Unified entry point
```

## 📦 Installation & Setup

### Prerequisites
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.11 or higher

### Step-by-Step
1. **Clone the repository**:
   ```bash
   git clone https://github.com/[your-username]/sentinel.git
   cd sentinel
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run_sentinel.py
   ```

5. **Access the Dashboard**:
   Open `http://localhost:5000` in your browser.
   - **Default Admin**: `admin`
   - **Default Password**: `admin123`

---

## 🔧 Technical Methodology
Sentinel operates at the **Operating System level**, allowing it to track and regulate all applications—including games and system tools—that browser-level extensions cannot reach.

- **Data Layer**: SQLite handles persistent storage for logs and configurations.
- **Enforcement Layer**: Uses `psutil` for process discovery and `pywin32` for system command calls (like session locking).
- **Concurrency**: Implements SQLite **WAL (Write-Ahead Logging)** mode to ensure the background monitor and the web dashboard can access the database simultaneously without conflict.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## 👥 Contributors
Developed by Anirban as part of a B.Tech Final Year Project.
