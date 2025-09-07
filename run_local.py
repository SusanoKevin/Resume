#!/usr/bin/env python3
"""
Local development server script
Run this file to start the Flask application locally
"""

import os
import sys

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    print("Loading environment variables from .env file...")
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# Import and run the Flask app
from main import app

if __name__ == "__main__":
    print("Starting Flask development server...")
    print("Visit http://localhost:5000 to view your resume")
    print("Visit http://localhost:5000/admin to manage content")
    print("Press Ctrl+C to stop the server")
    
    # Get configuration
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") == "development" or os.environ.get("DEBUG", "").lower() == "true"
    
    app.run(host="127.0.0.1", port=port, debug=debug_mode)