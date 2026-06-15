from flask import Blueprint, render_template, request, redirect, url_for, flash, abort # 👈 Added abort here
from flask_login import login_required, current_user # 👈 Added security track modules here
from app import db
from app.models import Inquiry

admissions_bp = Blueprint('admissions', __name__)

@admissions_bp.route('/')
def dashboard():
    # Fetch metrics for the dashboard
    total_inquiries = Inquiry.query.count()
    active_followups = Inquiry.query.filter_by(status='Follow-up').count()
    converted = Inquiry.query.filter_by(status='Converted').count()
    
    # Avoid division by zero
    conversion_rate = (converted / total_inquiries * 100) if total_inquiries > 0 else 0
    
    # Get all inquiries to display in a table
    all_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    
    return render_template(
        'admissions/dashboard.html', 
        total=total_inquiries, 
        followups=active_followups, 
        converted=converted, 
        rate=round(conversion_rate, 1),
        inquiries=all_inquiries
    )

@admissions_bp.route('/admissions/new', methods=['POST'])
@login_required
def add_inquiry():
    if current_user.role != 'Admin':
        abort(403)
        new_inquiry = Inquiry(
            student_name=request.form.get('student_name'),
            parent_name=request.form.get('parent_name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            target_class=request.form.get('target_class'),
            notes=request.form.get('notes'),
            status='Inquiry'
        )
        db.session.add(new_inquiry)
        db.session.commit()
        flash('New admission inquiry logged successfully!', 'success')
        return redirect(url_for('admissions.dashboard'))

@admissions_bp.route('/update_status/<int:inquiry_id>/<string:new_status>', methods=['POST'])
@login_required
def update_status(inquiry_id, new_status):
    if current_user.role != 'Admin':
        abort(403)
    from app.models import Inquiry
    from app import db
    
    # Locate the target inquiry lead
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    
    # Update status value dynamically
    inquiry.status = new_status
    db.session.commit()
    
    flash(f"Lead status for {inquiry.student_name} successfully updated to {new_status}!", "success")
    return redirect(url_for('admissions.dashboard'))