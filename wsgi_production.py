"""
Production WSGI entry point for Specimen Tracker
This file is configured for production deployment
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

# Production configuration
if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
