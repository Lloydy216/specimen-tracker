# Configuration file for Specimen Tracker
import os

# Python executable path
PYTHON_PATH = r"C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe"

# Flask configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

# Application settings
SECRET_KEY = os.getenv("SECRET_KEY", "dev")
APP_NAME = "Specimen Tracker"

# Startup script helper
def get_startup_command():
    """Returns the command to start the Flask application"""
    return f'"{PYTHON_PATH}" wsgi.py'

if __name__ == "__main__":
    print(f"Python Path: {PYTHON_PATH}")
    print(f"Startup Command: {get_startup_command()}")
    print(f"Flask URL: http://localhost:{FLASK_PORT}")
