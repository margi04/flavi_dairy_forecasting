# PostgreSQL Quick Start Guide for Flavi Dairy Forecasting AI

This guide will help you migrate your application from SQLite to PostgreSQL and connect it to your website.

## 🚀 Quick Setup (Automated)

### Step 1: Install PostgreSQL

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Install pgAdmin 4 when prompted (optional but recommended)

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 2: Run the Setup Script

```bash
python setup_postgresql.py
```

This script will:
- Create a PostgreSQL database named `flavi_dairy_forecasting`
- Create a user `flavi_user` with password `flavi_password_2024`
- Create a `.env` file with the database connection
- Migrate all your existing SQLite data to PostgreSQL
- Set up Flask-Migrate for future database changes

### Step 3: Start Your Application

```bash
python run.py
```

Your website will now use PostgreSQL instead of SQLite!

## 🔧 Manual Setup (If Automated Fails)

### Step 1: Create Database and User

Connect to PostgreSQL as the admin user:

```bash
psql -U postgres
```

Create the database and user:

```sql
CREATE DATABASE flavi_dairy_forecasting;
CREATE USER flavi_user WITH PASSWORD 'flavi_password_2024';
GRANT ALL PRIVILEGES ON DATABASE flavi_dairy_forecasting TO flavi_user;
\q
```

### Step 2: Create .env File

Create a `.env` file in your project root:

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://flavi_user:flavi_password_2024@localhost:5432/flavi_dairy_forecasting

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
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
```

### Step 3: Migrate Data

```bash
python migrate_to_postgresql.py
```

### Step 4: Set up Flask-Migrate

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📊 Verify Your Setup

### View PostgreSQL Database

```bash
python view_postgresql_database.py
```

### View SQLite Database (for comparison)

```bash
python view_database.py
```

## 🔗 Connect Your Website

Your Flask application is already configured to use PostgreSQL. The connection happens automatically through:

1. **Environment Variables**: The `DATABASE_URL` in your `.env` file
2. **Flask-SQLAlchemy**: Automatically connects using the URL
3. **Models**: All your existing models work with PostgreSQL

### Database Connection in Your Code

```python
# In config.py
if os.environ.get('DATABASE_URL'):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
```

## 🛠️ Troubleshooting

### Common Issues

**1. Connection Refused**
```
Error: could not connect to server: Connection refused
```
- Make sure PostgreSQL is running
- Check if the port is correct (default: 5432)

**2. Authentication Failed**
```
Error: FATAL: password authentication failed
```
- Verify the username and password in your `.env` file
- Make sure the user has proper permissions

**3. Database Does Not Exist**
```
Error: database "flavi_dairy_forecasting" does not exist
```
- Run the setup script again
- Or manually create the database

**4. Permission Denied**
```
Error: permission denied for table
```
- Grant proper permissions to the user
- Check if the user owns the database

### Useful Commands

**Start PostgreSQL (Windows):**
```bash
# If installed as a service, it should start automatically
# Otherwise, check Services app
```

**Start PostgreSQL (macOS/Linux):**
```bash
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

**Connect to PostgreSQL:**
```bash
psql -U flavi_user -d flavi_dairy_forecasting
```

**List databases:**
```sql
\l
```

**List tables:**
```sql
\dt
```

**View table structure:**
```sql
\d table_name
```

## 📈 Benefits of PostgreSQL

1. **Better Performance**: Handles large datasets more efficiently
2. **ACID Compliance**: Ensures data integrity
3. **Advanced Features**: JSON support, full-text search, etc.
4. **Scalability**: Can handle concurrent users better
5. **Production Ready**: Industry standard for web applications

## 🔄 Migration Back to SQLite (If Needed)

If you need to switch back to SQLite for development:

1. Update your `.env` file:
```env
# Comment out PostgreSQL URL
# DATABASE_URL=postgresql://...

# Use SQLite
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

2. Run your application:
```bash
python run.py
```

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify PostgreSQL is running: `psql --version`
3. Test connection: `psql -U flavi_user -d flavi_dairy_forecasting`
4. Check logs: `python view_postgresql_database.py`

## 🎉 Success!

Once you've completed the migration:

- ✅ Your data is safely stored in PostgreSQL
- ✅ Your website connects to PostgreSQL automatically
- ✅ All existing functionality works as before
- ✅ Better performance and scalability
- ✅ Production-ready database setup

Your Flavi Dairy Forecasting AI application is now running on PostgreSQL! 🚀 