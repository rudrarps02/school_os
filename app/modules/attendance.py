from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import AttendanceLog
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/')
def dashboard():
    today = datetime.utcnow().date()
    
    # Fetch real-time metrics for today
    today_records = AttendanceLog.query.filter_by(date=today).all()
    total_marked = len(today_records)
    presents = sum(1 for r in today_records if r.status == 'Present')
    absents = sum(1 for r in today_records if r.status == 'Absent')
    
    # Safely calculate daily presence rate
    attendance_rate = (presents / total_marked * 100) if total_marked > 0 else 0

    # Get all logs to show history table
    all_logs = AttendanceLog.query.order_by(AttendanceLog.date.desc()).all()

    return render_template(
        'attendance/dashboard.html',
        logs=all_logs,
        total=total_marked,
        presents=presents,
        absents=absents,
        rate=round(attendance_rate, 1),
        today=today
    )

@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    student = request.form.get('student_name')
    grade = request.form.get('target_class')
    status = request.form.get('status')
    remarks = request.form.get('remarks')
    
    # Build registration log entry
    new_log = AttendanceLog(
        student_name=student,
        target_class=grade,
        status=status,
        remarks=remarks
    )
    db.session.add(new_log)
    db.session.commit()
    
    flash(f"Successfully marked {student} as '{status}' for today!", "success")
    return redirect(url_for('attendance.dashboard'))