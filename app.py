import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# configure the database
# Use SQLite by default for local development
database_url = os.environ.get("DATABASE_URL", "sqlite:///resume.db")
# Fix PostgreSQL URL format if using Heroku or similar
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models  # noqa: F401
    import routes  # noqa: F401
    
    db.create_all()
    
    # Initialize with basic data if empty
    from models import PersonalInfo, Education, Experience, Skill, Project
    
    if not PersonalInfo.query.first():
        personal = PersonalInfo(
            name="Your Name",
            title="Professional Title",
            email="your.email@example.com",
            phone="(555) 123-4567",
            location="City, State",
            summary="Professional summary goes here. Update this in the admin panel.",
            linkedin_url="",
            github_url="",
            website_url=""
        )
        db.session.add(personal)
        db.session.commit()
