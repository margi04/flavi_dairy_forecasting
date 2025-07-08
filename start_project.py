import os
import subprocess
import sys

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def initialize_database():
    print("Initializing database with sample data...")
    subprocess.check_call([sys.executable, "init_db.py"])

def run_app():
    print("Starting Flask application...")
    subprocess.call([sys.executable, "run.py"])

if __name__ == "__main__":
    install_requirements()
    initialize_database()
    run_app() 