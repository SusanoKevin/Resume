from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import PersonalInfo, Education, Experience, Skill, Project, ContactMessage
from forms import PersonalInfoForm, EducationForm, ExperienceForm, SkillForm, ProjectForm, ContactForm

@app.route('/')
def resume():
    """Main resume display page"""
    personal = PersonalInfo.query.first()
    education = Education.query.order_by(Education.order_index.desc(), Education.start_date.desc()).all()
    experience = Experience.query.order_by(Experience.order_index.desc(), Experience.start_date.desc()).all()
    skills = Skill.query.order_by(Skill.category, Skill.order_index, Skill.name).all()
    projects = Project.query.order_by(Project.featured.desc(), Project.order_index.desc(), Project.start_date.desc()).all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category = skill.category or 'Other'
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    return render_template('resume.html', 
                         personal=personal,
                         education=education,
                         experience=experience,
                         skills_by_category=skills_by_category,
                         projects=projects)

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Thank you for your message! I will get back to you soon.', 'success')
    else:
        flash('Please fill out all required fields correctly.', 'danger')
    
    return redirect(url_for('resume') + '#contact')

@app.route('/admin')
def admin():
    """Admin dashboard"""
    personal = PersonalInfo.query.first()
    education_count = Education.query.count()
    experience_count = Experience.query.count()
    skills_count = Skill.query.count()
    projects_count = Project.query.count()
    messages_count = ContactMessage.query.filter_by(read=False).count()
    
    return render_template('admin.html',
                         personal=personal,
                         education_count=education_count,
                         experience_count=experience_count,
                         skills_count=skills_count,
                         projects_count=projects_count,
                         messages_count=messages_count)

@app.route('/admin/personal', methods=['GET', 'POST'])
def admin_personal():
    """Edit personal information"""
    personal = PersonalInfo.query.first()
    form = PersonalInfoForm(obj=personal)
    
    if form.validate_on_submit():
        if personal:
            form.populate_obj(personal)
        else:
            personal = PersonalInfo()
            form.populate_obj(personal)
            db.session.add(personal)
        
        db.session.commit()
        flash('Personal information updated successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('admin_section.html', 
                         title='Personal Information',
                         form=form,
                         section='personal')

@app.route('/admin/education')
def admin_education():
    """Manage education entries"""
    education = Education.query.order_by(Education.order_index.desc(), Education.start_date.desc()).all()
    return render_template('admin_section.html',
                         title='Education',
                         items=education,
                         section='education')

@app.route('/admin/education/new', methods=['GET', 'POST'])
@app.route('/admin/education/<int:id>/edit', methods=['GET', 'POST'])
def admin_education_form(id=None):
    """Add or edit education entry"""
    if id:
        education = Education.query.get_or_404(id)
        form = EducationForm(obj=education)
    else:
        education = None
        form = EducationForm()
    
    if form.validate_on_submit():
        if education:
            form.populate_obj(education)
        else:
            education = Education()
            form.populate_obj(education)
            db.session.add(education)
        
        db.session.commit()
        flash('Education entry saved successfully!', 'success')
        return redirect(url_for('admin_education'))
    
    return render_template('admin_section.html',
                         title='Education Entry',
                         form=form,
                         section='education')

@app.route('/admin/education/<int:id>/delete', methods=['POST'])
def admin_education_delete(id):
    """Delete education entry"""
    education = Education.query.get_or_404(id)
    db.session.delete(education)
    db.session.commit()
    flash('Education entry deleted successfully!', 'success')
    return redirect(url_for('admin_education'))

@app.route('/admin/experience')
def admin_experience():
    """Manage experience entries"""
    experience = Experience.query.order_by(Experience.order_index.desc(), Experience.start_date.desc()).all()
    return render_template('admin_section.html',
                         title='Experience',
                         items=experience,
                         section='experience')

@app.route('/admin/experience/new', methods=['GET', 'POST'])
@app.route('/admin/experience/<int:id>/edit', methods=['GET', 'POST'])
def admin_experience_form(id=None):
    """Add or edit experience entry"""
    if id:
        experience = Experience.query.get_or_404(id)
        form = ExperienceForm(obj=experience)
    else:
        experience = None
        form = ExperienceForm()
    
    if form.validate_on_submit():
        if experience:
            form.populate_obj(experience)
        else:
            experience = Experience()
            form.populate_obj(experience)
            db.session.add(experience)
        
        db.session.commit()
        flash('Experience entry saved successfully!', 'success')
        return redirect(url_for('admin_experience'))
    
    return render_template('admin_section.html',
                         title='Experience Entry',
                         form=form,
                         section='experience')

@app.route('/admin/experience/<int:id>/delete', methods=['POST'])
def admin_experience_delete(id):
    """Delete experience entry"""
    experience = Experience.query.get_or_404(id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience entry deleted successfully!', 'success')
    return redirect(url_for('admin_experience'))

@app.route('/admin/skills')
def admin_skills():
    """Manage skills"""
    skills = Skill.query.order_by(Skill.category, Skill.order_index, Skill.name).all()
    return render_template('admin_section.html',
                         title='Skills',
                         items=skills,
                         section='skills')

@app.route('/admin/skills/new', methods=['GET', 'POST'])
@app.route('/admin/skills/<int:id>/edit', methods=['GET', 'POST'])
def admin_skills_form(id=None):
    """Add or edit skill"""
    if id:
        skill = Skill.query.get_or_404(id)
        form = SkillForm(obj=skill)
    else:
        skill = None
        form = SkillForm()
    
    if form.validate_on_submit():
        if skill:
            form.populate_obj(skill)
        else:
            skill = Skill()
            form.populate_obj(skill)
            db.session.add(skill)
        
        db.session.commit()
        flash('Skill saved successfully!', 'success')
        return redirect(url_for('admin_skills'))
    
    return render_template('admin_section.html',
                         title='Skill Entry',
                         form=form,
                         section='skills')

@app.route('/admin/skills/<int:id>/delete', methods=['POST'])
def admin_skills_delete(id):
    """Delete skill"""
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_skills'))

@app.route('/admin/projects')
def admin_projects():
    """Manage projects"""
    projects = Project.query.order_by(Project.featured.desc(), Project.order_index.desc(), Project.start_date.desc()).all()
    return render_template('admin_section.html',
                         title='Projects',
                         items=projects,
                         section='projects')

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@app.route('/admin/projects/<int:id>/edit', methods=['GET', 'POST'])
def admin_projects_form(id=None):
    """Add or edit project"""
    if id:
        project = Project.query.get_or_404(id)
        form = ProjectForm(obj=project)
    else:
        project = None
        form = ProjectForm()
    
    if form.validate_on_submit():
        if project:
            form.populate_obj(project)
        else:
            project = Project()
            form.populate_obj(project)
            db.session.add(project)
        
        db.session.commit()
        flash('Project saved successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin_section.html',
                         title='Project Entry',
                         form=form,
                         section='projects')

@app.route('/admin/projects/<int:id>/delete', methods=['POST'])
def admin_projects_delete(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/messages')
def admin_messages():
    """View contact messages"""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    # Mark all as read
    ContactMessage.query.update({ContactMessage.read: True})
    db.session.commit()
    
    return render_template('admin_section.html',
                         title='Contact Messages',
                         items=messages,
                         section='messages')
