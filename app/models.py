from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='Viewer') # Can be 'Admin' or 'Viewer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"


class Inquiry(db.Model):
    __tablename__ = 'inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    target_class = db.Column(db.String(50), nullable=False)
    
    # Pipeline tracking status: 'Inquiry', 'Follow-up', 'Converted', 'Closed'
    status = db.Column(db.String(20), default='Inquiry') 
    
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Inquiry {self.student_name} - {self.status}>"
    
class FeeStructure(db.Model):
    __tablename__ = 'fee_structures'
    
    id = db.Column(db.Integer, primary_key=True)
    target_class = db.Column(db.String(50), unique=True, nullable=False)
    admission_fee = db.Column(db.Float, default=0.0)
    tuition_fee = db.Column(db.Float, default=0.0)
    transport_fee = db.Column(db.Float, default=0.0)
    
    @property
    def total_fee(self):
        return self.admission_fee + self.tuition_fee + self.transport_fee


class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    target_class = db.Column(db.String(50), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(20), default='Cash') # Cash, Card, UPI, NetBanking
    reference_no = db.Column(db.String(50), nullable=True) # Transaction/Check IDs
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)

class AttendanceLog(db.Model):
    __tablename__ = 'attendance_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    target_class = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Status can be: 'Present', 'Absent', or 'Late'
    status = db.Column(db.String(20), default='Present')
    remarks = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Attendance {self.student_name} - {self.date} - {self.status}>"
    
class ExamResult(db.Model):
    __tablename__ = 'exam_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    target_class = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False) # e.g., Mathematics, Science
    exam_type = db.Column(db.String(50), default='Term 1') # e.g., Mid-Term, Final Exam
    marks_obtained = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, default=100.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def percentage(self):
        if self.max_marks > 0:
            return (self.marks_obtained / self.max_marks) * 100
        return 0.0

    @property
    def grade(self):
        pct = self.percentage
        if pct >= 90: return 'A+'
        elif pct >= 80: return 'A'
        elif pct >= 70: return 'B'
        elif pct >= 60: return 'C'
        elif pct >= 40: return 'D'
        else: return 'F (Fail)'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    target_class = db.Column(db.String(50), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    parent_phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), default='Active') # Active, Graduated, Suspended
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Student {self.admission_no} - {self.full_name}>"