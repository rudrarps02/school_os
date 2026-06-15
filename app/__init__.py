from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

import os
from dotenv import load_dotenv

load_dotenv() # Loads the .env file contents


def create_app():
    app = Flask(__name__)
    
    # # 1. App Configuration (Now dynamically loading safely from your secrets file!)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'schoolos-super-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///school.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # # 2. Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # 3. Import ALL Models so db.create_all() catches them
    from app.models import User, Inquiry, FeeStructure, FeePayment, AttendanceLog, ExamResult, Student

    # 4. Create Database Tables Automatically
    with app.app_context():
        db.create_all()

    # # 5. Register All Blueprints (Cleanly grouped at the bottom)
    from app.modules.auth import auth
    from app.modules.admissions import admissions_bp
    from app.modules.fees import fees_bp
    from app.modules.attendance import attendance_bp
    from app.modules.exams import exams_bp
    from app.modules.students import students_bp

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admissions_bp, url_prefix='/admissions')
    app.register_blueprint(fees_bp, url_prefix='/fees')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(exams_bp, url_prefix='/exams')
    app.register_blueprint(students_bp, url_prefix='/students')


    @app.route('/')
    @login_required 
    def home():
        # Import models locally inside the function to prevent circular dependency bugs
        from app.models import Inquiry, Student, FeePayment, AttendanceLog

        # Gather live aggregate data points across all tracking tables
        total_admissions_leads = Inquiry.query.count()
        active_students_count = Student.query.count()
        
        # Calculate Total Revenue Collected
        payments = FeePayment.query.all()
        total_revenue = sum(p.amount_paid for p in payments)
        
        # Calculate Daily Attendance Rate safely
        attendance_records = AttendanceLog.query.all()
        total_days_logged = len(attendance_records)
        days_present = sum(1 for log in attendance_records if log.status == 'Present')
        global_attendance_rate = (days_present / total_days_logged * 100) if total_days_logged > 0 else 0.0

        return render_template(
            'index.html',
            leads=total_admissions_leads,
            students=active_students_count,
            revenue=total_revenue,
            attendance_rate=round(global_attendance_rate, 1)
        )

    return app # This should be the absolute last line of your create_app() function
