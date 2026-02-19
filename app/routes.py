import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, send_from_directory, current_app
from app import db, bcrypt
from app.models import User, Document
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# --- CONFIGURATION ---
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

# --------------------------
# Authentication Routes
# --------------------------

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html')

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --------------------------
# Dashboard, Admin & File Routes
# --------------------------

@main.route("/dashboard")
@login_required
def dashboard():
    # Search Logic
    q = request.args.get('q')
    if q:
        documents = Document.query.filter(
            Document.user_id == current_user.id, 
            Document.filename.contains(q)
        ).all()
    else:
        documents = Document.query.filter_by(user_id=current_user.id).all()
        
    return render_template('dashboard.html', documents=documents)

@main.route("/admin")
@login_required
def admin():
    # Security Check: Only allow 'admin' role
    if current_user.role != 'admin':
        flash('Access denied. Administrators only.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Load ALL data for the admin view
    users = User.query.all()
    all_docs = Document.query.all()
    return render_template('admin.html', users=users, documents=all_docs)

@main.route("/upload", methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.dashboard'))
        
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        new_doc = Document(filename=filename, filepath=save_path, author=current_user)
        db.session.add(new_doc)
        db.session.commit()
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid file type! Allowed types: PDF, PNG, JPG, DOCX, TXT', 'danger')
        return redirect(url_for('main.dashboard'))

@main.route("/download/<int:file_id>")
@login_required
def download_file(file_id):
    doc = Document.query.get_or_404(file_id)
    
    # Allow download if user is owner OR user is admin
    if doc.author != current_user and current_user.role != 'admin':
        flash('You do not have permission to view this file.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], doc.filename, as_attachment=True)

@main.route("/delete/<int:file_id>")
@login_required
def delete_file(file_id):
    doc = Document.query.get_or_404(file_id)
    
    if doc.author != current_user and current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(doc)
    db.session.commit()
    
    try:
        if os.path.exists(doc.filepath):
            os.remove(doc.filepath)
            flash('File deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting file from disk: {e}', 'warning')
        
    return redirect(url_for('main.dashboard'))