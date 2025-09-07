# Interactive Resume Website

A modern, responsive resume website built with Flask and PostgreSQL, featuring a comprehensive admin panel for content management.

## Features

- **Interactive Resume Display**: Professional resume layout with timeline animations
- **Admin Panel**: Full CRUD operations for managing resume content
- **Database Management**: PostgreSQL integration for data persistence
- **Responsive Design**: Mobile-friendly Bootstrap dark theme
- **Contact Form**: Functional contact form with database storage
- **Print-Optimized**: Print-friendly CSS for PDF generation

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-WTF
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, Custom CSS, Vanilla JavaScript

## Local Development

1. Clone the repository
2. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SESSION_SECRET`: Flask session secret key
3. Run the application: `python main.py`

## Admin Access

Visit `/admin` to access the content management system where you can:
- Update personal information
- Manage work experience
- Add/edit education entries
- Configure skills and proficiency levels
- Showcase projects
- View contact form submissions

## Database Schema

- **PersonalInfo**: Contact details and professional summary
- **Experience**: Work history with timeline features
- **Education**: Academic background
- **Skill**: Technical and soft skills with categories
- **Project**: Portfolio projects
- **ContactMessage**: Contact form submissions
