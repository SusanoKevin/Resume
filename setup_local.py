#!/usr/bin/env python3
"""
Setup script for local development
This script helps set up the Flask application for local development
"""

import os
import sys
import subprocess

def install_requirements():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "local_requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Make sure you have pip installed and try again")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Flask configuration
FLASK_ENV=development
DEBUG=true
SESSION_SECRET=dev-secret-key-change-in-production

# Database configuration (uses SQLite by default)
DATABASE_URL=sqlite:///resume.db

# Port configuration
PORT=5000
""")
        print("✅ Created .env file with default settings")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up Flask Resume Application for Local Development")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete!")
    print("\nTo start the application:")
    print("  python run_local.py")
    print("\nOr use the standard Flask command:")
    print("  python main.py")
    print("\nYour resume will be available at: http://localhost:5000")
    print("Admin panel will be available at: http://localhost:5000/admin")

if __name__ == "__main__":
    main()