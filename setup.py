import os
import subprocess
import sys

def setup_environment():
    # Create .env file
    env_content = """FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=flavi-dairy-solutions-secret-key-2024
DATABASE_URL=sqlite:///app.db"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Environment variables set up successfully!")

def initialize_database():
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            db.create_all()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

def run_application():
    try:
        subprocess.run([sys.executable, 'run.py'])
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == '__main__':
    setup_environment()
    initialize_database()
    run_application() 