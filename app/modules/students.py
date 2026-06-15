from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Student, AttendanceLog, ExamResult, FeePayment

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
def directory():
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        all_students = Student.query.filter(Student.full_name.ilike(f"%{search_query}%")).all()
    else:
        all_students = Student.query.order_by(Student.admission_no.asc()).all()
        
    total_enrolled = len(all_students)
    return render_template('students/directory.html', students=all_students, total=total_enrolled, search_query=search_query)

@students_bp.route('/register', methods=['POST'])
def register_student():
    adm_no = request.form.get('admission_no')
    name = request.form.get('full_name')
    grade = request.form.get('target_class')
    parent = request.form.get('parent_name')
    phone = request.form.get('parent_phone')

    existing = Student.query.filter_by(admission_no=adm_no).first()
    if existing:
        flash(f"Admission Number {adm_no} is already assigned to a student!", "danger")
        return redirect(url_for('students.directory'))

    new_student = Student(
        admission_no=adm_no, full_name=name,
        target_class=grade, parent_name=parent, parent_phone=phone
    )
    db.session.add(new_student)
    db.session.commit()
    
    flash(f"Successfully generated permanent profile roster for {name}!", "success")
    return redirect(url_for('students.directory'))

@students_bp.route('/profile/<int:student_id>')
def view_profile(student_id):
    student = Student.query.get_or_404(student_id)
    
    attendance_history = AttendanceLog.query.filter_by(student_name=student.full_name).all()
    academic_history = ExamResult.query.filter_by(student_name=student.full_name).all()
    payments_history = FeePayment.query.filter_by(student_name=student.full_name).all()
    
    total_days = len(attendance_history)
    days_present = sum(1 for r in attendance_history if r.status == 'Present')
    attendance_rate = (days_present / total_days * 100) if total_days > 0 else 100.0
    
    total_fees_paid = sum(p.amount_paid for p in payments_history)

    return render_template(
        'students/profile.html',
        student=student,
        attendance=attendance_history,
        academics=academic_history,
        payments=payments_history,
        attendance_rate=round(attendance_rate, 1),
        total_paid=total_fees_paid
    )