# Project Report: Sentinel Parental Control System

## 1. Abstract
The "Sentinel Parental Control and Application Monitoring System" is a software solution designed to help parents manage and monitor their children's digital activities on Windows-based PCs. Unlike browser-level extensions, Sentinel operates at the operating system level, ensuring that all applications—including games and system tools—are tracked and regulated. The system features a background enforcement engine and a remote-accessible web dashboard for real-time management.

## 2. Objectives
- To provide a reliable, silent background service for tracking application usage.
- To implement a blacklist-based application blocking mechanism.
- To enforce daily screen time limits to prevent excessive computer usage.
- To offer a user-friendly, responsive dashboard for parents to view analytics and manage settings.

## 3. System Requirements
### 3.1 Hardware Requirements
- **Processor**: Intel Core i3 or equivalent (minimum).
- **RAM**: 4GB (minimum).
- **Storage**: 100MB of free disk space for logs and database.

### 3.2 Software Requirements
- **Operating System**: Windows 10/11 (64-bit).
- **Runtime**: Python 3.11+.
- **Database**: SQLite 3.

## 4. Methodology
The project follows a modular architecture:
- **Data Layer**: SQLite handles persistent storage of logs and configurations.
- **Enforcement Layer**: Uses `psutil` for process discovery and `pywin32` for session locking.
- **Management Layer**: A Flask web server provides an interface for parents to interact with the system logic.
