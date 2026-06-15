from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import FeeStructure, FeePayment

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/')
def dashboard():
    # 1. Calculate Summary Metrics
    all_payments = FeePayment.query.order_by(FeePayment.paid_at.desc()).all()
    total_revenue = sum(payment.amount_paid for payment in all_payments)
    
    # Get configuration collections to show options
    structures = FeeStructure.query.all()
    
    return render_template(
        'fees/dashboard.html',
        payments=all_payments,
        revenue=total_revenue,
        structures=structures
    )

@fees_bp.route('/setup-structure', methods=['POST'])
def setup_structure():
    grade = request.form.get('target_class')
    admission = float(request.form.get('admission_fee', 0))
    tuition = float(request.form.get('tuition_fee', 0))
    transport = float(request.form.get('transport_fee', 0))
    
    # Check if a setup for this class already exists
    existing = FeeStructure.query.filter_by(target_class=grade).first()
    if existing:
        existing.admission_fee = admission
        existing.tuition_fee = tuition
        existing.transport_fee = transport
        flash(f"Updated fee structure configurations for {grade}!", "success")
    else:
        new_structure = FeeStructure(
            target_class=grade, admission_fee=admission, 
            tuition_fee=tuition, transport_fee=transport
        )
        db.session.add(new_structure)
        flash(f"Configured new fee structure for {grade} successfully!", "success")
        
    db.session.commit()
    return redirect(url_for('fees.dashboard'))

@fees_bp.route('/collect', methods=['POST'])
def collect_fee():
    student = request.form.get('student_name')
    grade = request.form.get('target_class')
    amount = float(request.form.get('amount_paid', 0))
    mode = request.form.get('payment_mode')
    ref = request.form.get('reference_no')
    
    new_receipt = FeePayment(
        student_name=student, target_class=grade,
        amount_paid=amount, payment_mode=mode, reference_no=ref
    )
    db.session.add(new_receipt)
    db.session.commit()
    
    flash(f"Successfully processed payment receipt of ₹{amount} for {student}!", "success")
    return redirect(url_for('fees.dashboard'))