from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Hashed password
    role = db.Column(db.String(10), default='user') # 'user' or 'admin'
    
    # Relationship: One User can have Many Documents
    documents = db.relationship('Document', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False) # Original name
    filepath = db.Column(db.String(200), nullable=False) # Storage path
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Key: Link to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Document('{self.filename}', '{self.upload_date}')"