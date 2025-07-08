# PostgreSQL Setup Script for Flavi Dairy AI
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Setup for Flavi Dairy AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if PostgreSQL is installed
Write-Host "Step 1: Checking if PostgreSQL is installed..." -ForegroundColor Yellow
try {
    $psqlVersion = psql --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PostgreSQL is installed" -ForegroundColor Green
        Write-Host "Version: $psqlVersion" -ForegroundColor Gray
    } else {
        throw "PostgreSQL not found"
    }
} catch {
    Write-Host "❌ PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install PostgreSQL first from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Setting up database and user..." -ForegroundColor Yellow
Write-Host "Please enter the password for the postgres user when prompted:" -ForegroundColor Cyan

# Create database and user
Write-Host "Creating database..." -ForegroundColor Gray
psql -U postgres -c "CREATE DATABASE flavi_dairy_forecasting;" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Database might already exist, continuing..." -ForegroundColor Yellow
}

Write-Host "Creating user..." -ForegroundColor Gray
psql -U postgres -c "CREATE USER flavi_user WITH PASSWORD 'flavi_password_2024';" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  User might already exist, continuing..." -ForegroundColor Yellow
}

Write-Host "Granting privileges..." -ForegroundColor Gray
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE flavi_dairy_forecasting TO flavi_user;" 2>$null

Write-Host "✅ Database setup completed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Creating .env file..." -ForegroundColor Yellow

# Create .env file content
$envContent = @"
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://flavi_user:flavi_password_2024@localhost:5432/flavi_dairy_forecasting

# Flask Configuration
SECRET_KEY=flavi-dairy-secret-key-2024-change-in-production
FLASK_ENV=development
FLASK_DEBUG=1

# Email Configuration (optional)
MAIL_SERVER=localhost
MAIL_PORT=8025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@flavi.com
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ .env file created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Migrating data from SQLite to PostgreSQL..." -ForegroundColor Yellow
python migrate_to_postgresql.py

Write-Host ""
Write-Host "Step 5: Testing connection..." -ForegroundColor Yellow
python test_postgresql_connection.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now:" -ForegroundColor White
Write-Host "1. View your data: python view_postgresql_data.py" -ForegroundColor Cyan
Write-Host "2. Start your website: python run.py" -ForegroundColor Cyan
Write-Host "3. Use pgAdmin 4 to manage your database" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue" 