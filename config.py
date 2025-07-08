import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Database Configuration - PostgreSQL for production, SQLite for development
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML Model Settings
    FORECAST_HORIZON_DAYS = 30
    TRAINING_DATA_DAYS = 365  # Use 1 year of data for training
    
    # Application Settings
    ITEMS_PER_PAGE = 20
    MAX_FORECAST_DAYS = 90  # Maximum number of days to forecast
    
    # Flask-Mail configuration
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'noreply@flavi.com' 