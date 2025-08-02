from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db, login_manager

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/')
def home_redirect():
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role'].lower()

        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect('/admin')
            elif user.role == 'agent':
                return redirect('/agent')
            else:
                return redirect('/dashboard')
        else:
            flash('Invalid credentials.')
            return redirect(url_for('auth.login'))

    return render_template('index.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
