from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from ..extensions import db, bcrypt
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak sama.', 'danger')
            return render_template('register.html') # Anda perlu membuat template register.html
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Akun Anda berhasil dibuat! Anda sekarang bisa login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registrasi gagal. Username atau Email mungkin sudah terdaftar. Error: {e}', 'danger')
            return render_template('register.html') # Anda perlu membuat template register.html
    return render_template('register.html') # Anda perlu membuat template register.html

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False # Checkbox "Ingat saya"

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Login berhasil!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login gagal. Periksa email dan password Anda.', 'danger')
    return render_template('login.html') # Anda perlu membuat template login.html

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('main.home'))
