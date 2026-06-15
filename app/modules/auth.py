from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username_input = request.form.get('username', '').strip()
        password_input = request.form.get('password')

        # Locate user via database username ledger
        user = User.query.filter_by(username=username_input).first()

        # Securely verify password hash match
        if user and check_password_hash(user.password_hash, password_input):
            login_user(user)
            flash(f"Welcome back, {user.username}! Active Profile Role: [{user.role}]", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please check your username and password.", "danger")
            
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_input = request.form.get('username', '').strip()
        password_input = request.form.get('password')
        role_input = request.form.get('role', 'Viewer') # Defaults to Viewer role

        user_exists = User.query.filter_by(username=username_input).first()
        if user_exists:
            flash("Username already exists in the system directory.", "danger")
            return redirect(url_for('auth.register'))

        # Securely hash password before writing to SQLite storage layers
        hashed_password = generate_password_hash(password_input, method='pbkdf2:sha256')
        
        new_user = User(
            username=username_input,
            password_hash=hashed_password,
            role=role_input
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account registration processed successfully! Please sign in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Session terminated successfully. Administrative credentials cleared.", "info")
    return redirect(url_for('auth.login'))