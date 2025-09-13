# Specimen Tracker

A Flask-based web application for tracking patient specimens, samples, and test orders in medical laboratories.

## 🌐 Live Application

**Your teacher can access the live application at:**
- **Live URL**: [Your Railway URL will go here]
- **Status**: ✅ Deployed and running on Railway
- **Features**: All functionality available online

## Quick Start

### Option 1: Double-click to start (Recommended)
Simply double-click `start_app.bat` to start the application. This will:
- Start the Flask server on http://localhost:5000
- Open your browser automatically
- Use the correct Python environment

### Option 2: PowerShell
Run `start_app.ps1` in PowerShell for a more detailed startup experience.

### Option 3: Manual startup
```bash
# Navigate to project directory
cd C:\Users\findl\Desktop\specimen_tracker

# Start Flask application
C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe wsgi.py
```

## Features

- **Patient Management**: Add, view, and manage patient information
- **Sample Tracking**: Track specimen samples through the laboratory
- **Test Orders**: Manage laboratory test orders and results
- **Modern UI**: Responsive web interface with clean design

## Requirements

- Python 3.13
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.7

## Installation

Dependencies are already installed in the Python environment at:
`C:\Users\findl\AppData\Local\Programs\Python\Python313\`

## Troubleshooting

### "No module named 'flask'" error
This happens when using the wrong Python interpreter. Always use:
`C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe`

### Port 5000 already in use
If you see this error, another instance might be running. Check with:
```powershell
netstat -an | Select-String ":5000"
```

### Application won't start
1. Ensure you're in the correct directory
2. Use the provided startup scripts
3. Check that Python 3.13 is installed

## Development

The application runs in debug mode by default, so any code changes will automatically reload the server.

## Access

### Live Deployment (Railway)
- **Live URL**: [Your Railway URL will go here]
- **Status**: ✅ Deployed and running
- **Database**: PostgreSQL (production)
- **Security**: HTTPS enabled

### Local Development
Once started locally, access your application at:
- **Local**: http://localhost:5000
- **Network**: http://192.168.0.19:5000 (if accessible from other devices)

## Deployment

This application is deployed on Railway with:
- **Platform**: Railway.app
- **Database**: PostgreSQL
- **Web Server**: Gunicorn
- **Environment**: Production
