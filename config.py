import os

from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
 
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') 
    # or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False

    """Cloudinary config variables"""
    CLOUDINARY_CLOUD_NAME  = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY  = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET  = os.getenv("CLOUDINARY_API_SECRET") 