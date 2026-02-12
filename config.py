import os

# Get the absolute path of the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Security Key (Keep this secret in production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    
    # Database Configuration (SQLite)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'secure_docs.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit uploads to 16MB