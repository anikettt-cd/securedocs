import os
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default='user')
    documents = db.relationship('Document', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def icon_class(self):
        # Determine icon based on file extension
        ext = os.path.splitext(self.filename)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'fa-file-image text-primary'  # Blue Image Icon
        elif ext == '.pdf':
            return 'fa-file-pdf text-danger'     # Red PDF Icon
        elif ext == '.txt':
            return 'fa-file-alt text-secondary'  # Gray Text Icon
        elif ext == '.docx':
            return 'fa-file-word text-primary'   # Blue Word Icon
        else:
            return 'fa-file text-muted'          # Default Icon

    def __repr__(self):
        return f"Document('{self.filename}', '{self.upload_date}')"