from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, URL, Optional

class PersonalInfoForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    title = StringField('Professional Title', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    location = StringField('Location')
    summary = TextAreaField('Professional Summary')
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    website_url = StringField('Website URL', validators=[Optional(), URL()])
    submit = SubmitField('Update Personal Info')

class EducationForm(FlaskForm):
    institution = StringField('Institution', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    field_of_study = StringField('Field of Study')
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    gpa = StringField('GPA')
    description = TextAreaField('Description')
    order_index = IntegerField('Order', default=0)
    submit = SubmitField('Save Education')

class ExperienceForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    location = StringField('Location')
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    current = BooleanField('Current Position')
    description = TextAreaField('Description')
    achievements = TextAreaField('Key Achievements')
    order_index = IntegerField('Order', default=0)
    submit = SubmitField('Save Experience')

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Technical', 'Technical'),
        ('Programming', 'Programming'),
        ('Software', 'Software'),
        ('Languages', 'Languages'),
        ('Soft Skills', 'Soft Skills'),
        ('Other', 'Other')
    ])
    proficiency = IntegerField('Proficiency (0-100)', validators=[NumberRange(min=0, max=100)], default=50)
    order_index = IntegerField('Order', default=0)
    submit = SubmitField('Save Skill')

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    technologies = StringField('Technologies (comma-separated)')
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    live_url = StringField('Live Demo URL', validators=[Optional(), URL()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    featured = BooleanField('Featured Project')
    order_index = IntegerField('Order', default=0)
    submit = SubmitField('Save Project')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
