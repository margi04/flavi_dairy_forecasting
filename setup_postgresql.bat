@echo off
echo ========================================
echo PostgreSQL Setup for Flavi Dairy AI
echo ========================================
echo.

echo Step 1: Checking if PostgreSQL is installed...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL first from: https://www.postgresql.org/download/windows/
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
) else (
    echo ✅ PostgreSQL is installed
)

echo.
echo Step 2: Setting up database and user...
echo Please enter the password for the postgres user when prompted:
echo.

REM Create database and user
psql -U postgres -c "CREATE DATABASE flavi_dairy_forecasting;" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Database might already exist, continuing...
)

psql -U postgres -c "CREATE USER flavi_user WITH PASSWORD 'flavi_password_2024';" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  User might already exist, continuing...
)

psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE flavi_dairy_forecasting TO flavi_user;" 2>nul

echo ✅ Database setup completed
echo.

echo Step 3: Creating .env file...
(
echo # PostgreSQL Database Configuration
echo DATABASE_URL=postgresql://flavi_user:flavi_password_2024@localhost:5432/flavi_dairy_forecasting
echo.
echo # Flask Configuration
echo SECRET_KEY=flavi-dairy-secret-key-2024-change-in-production
echo FLASK_ENV=development
echo FLASK_DEBUG=1
echo.
echo # Email Configuration ^(optional^)
echo MAIL_SERVER=localhost
echo MAIL_PORT=8025
echo MAIL_USE_TLS=False
echo MAIL_USE_SSL=False
echo MAIL_USERNAME=
echo MAIL_PASSWORD=
echo MAIL_DEFAULT_SENDER=noreply@flavi.com
) > .env

echo ✅ .env file created
echo.

echo Step 4: Migrating data from SQLite to PostgreSQL...
python migrate_to_postgresql.py

echo.
echo Step 5: Testing connection...
python test_postgresql_connection.py

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo You can now:
echo 1. View your data: python view_postgresql_data.py
echo 2. Start your website: python run.py
echo 3. Use pgAdmin 4 to manage your database
echo.
pause