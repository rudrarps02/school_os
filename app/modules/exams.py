from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import ExamResult

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/')
def dashboard():
    # Fetch all grade sheets recorded so far
    all_results = ExamResult.query.order_by(ExamResult.created_at.desc()).all()
    
    # Simple aggregated system stats
    total_papers_graded = len(all_results)
    failures = sum(1 for r in all_results if r.grade == 'F (Fail)')
    pass_rate = ((total_papers_graded - failures) / total_papers_graded * 100) if total_papers_graded > 0 else 100.0

    return render_template(
        'exams/dashboard.html',
        results=all_results,
        total_graded=total_papers_graded,
        pass_rate=round(pass_rate, 1)
    )

@exams_bp.route('/add-mark', methods=['POST'])
def add_mark():
    student = request.form.get('student_name')
    grade = request.form.get('target_class')
    subject = request.form.get('subject')
    exam = request.form.get('exam_type')
    obtained = float(request.form.get('marks_obtained', 0))
    maximum = float(request.form.get('max_marks', 100))
    
    if obtained > maximum:
        flash("Error: Obtained marks cannot be greater than maximum possible marks!", "danger")
        return redirect(url_for('exams.dashboard'))

    new_report = ExamResult(
        student_name=student, target_class=grade,
        subject=subject, exam_type=exam,
        marks_obtained=obtained, max_marks=maximum
    )
    db.session.add(new_report)
    db.session.commit()
    
    flash(f"Successfully published grade card sheet entry for {student}!", "success")
    return redirect(url_for('exams.dashboard'))