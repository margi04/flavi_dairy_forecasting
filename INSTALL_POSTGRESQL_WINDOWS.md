# PostgreSQL Installation & Migration Guide for Windows

## 🚀 Quick Installation Steps

### Step 1: Download PostgreSQL

1. **Go to:** https://www.postgresql.org/download/windows/
2. **Click:** "Download the installer"
3. **Choose:** Latest version (16.x) for Windows x86-64
4. **Download:** The .exe installer file

### Step 2: Install PostgreSQL

1. **Run the installer** as Administrator
2. **Use these settings:**
   - Installation Directory: `C:\Program Files\PostgreSQL\16\` (default)
   - Data Directory: `C:\Program Files\PostgreSQL\16\data` (default)
   - **Password for postgres user:** `postgres123` (remember this!)
   - Port: `5432` (default)
   - Locale: `Default locale` (default)
   - **✅ Install pgAdmin 4** (check this box)
   - **❌ Stack Builder** (uncheck this box)

3. **Complete the installation**

### Step 3: Add PostgreSQL to PATH

After installation, add PostgreSQL to your system PATH:

1. **Open System Properties:**
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"

2. **Edit PATH:**
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Program Files\PostgreSQL\16\bin`
   - Click "OK" on all dialogs

3. **Restart Command Prompt/PowerShell**

### Step 4: Test Installation

Open a new Command Prompt or PowerShell and run:

```bash
psql --version
```

You should see the PostgreSQL version.

### Step 5: Run the Migration Script

Once PostgreSQL is installed and in PATH:

```bash
# Option 1: Using batch file
setup_postgresql.bat

# Option 2: Using PowerShell script
.\setup_postgresql.ps1

# Option 3: Manual setup
python setup_postgresql.py
```

## 🔄 What Happens During Migration

The migration process will:

1. **Create Database:**
   - Database name: `flavi_dairy_forecasting`
   - User: `flavi_user`
   - Password: `flavi_password_2024`

2. **Migrate Data:**
   - Copy all tables from SQLite to PostgreSQL
   - Preserve all relationships and data types
   - Maintain data integrity

3. **Update Configuration:**
   - Create `.env` file with PostgreSQL connection
   - Configure Flask to use PostgreSQL
   - Keep all existing functionality

4. **Test Setup:**
   - Verify connection works
   - Confirm data migration was successful
   - Test Flask-SQLAlchemy integration

## 📊 Your Current Data

Based on your SQLite database, you have:
- Database file: `instance/app.db` (532 KB)
- Contains your existing data (users, customers, SKUs, sales, inventory)

This data will be safely migrated to PostgreSQL.

## 🎯 After Migration

Once complete, you'll have:

✅ **Better Performance:** PostgreSQL handles large datasets more efficiently
✅ **Scalability:** Can handle multiple concurrent users
✅ **Data Integrity:** ACID compliance ensures data consistency
✅ **Professional Tools:** pgAdmin 4 for database management
✅ **Production Ready:** Industry standard for web applications

## 🔧 Troubleshooting

### If psql command not found:
1. Make sure PostgreSQL is installed
2. Add PostgreSQL bin directory to PATH
3. Restart Command Prompt/PowerShell

### If installation fails:
1. Run installer as Administrator
2. Check Windows Defender/Firewall settings
3. Ensure port 5432 is not in use

### If migration fails:
1. Check PostgreSQL is running
2. Verify database user permissions
3. Check .env file configuration

## 📋 Verification Commands

After setup, verify everything works:

```bash
# Test PostgreSQL connection
python test_postgresql_connection.py

# View your data
python view_postgresql_data.py

# Start your website
python run.py
```

## 🎉 Success Indicators

You'll know it's working when:

1. ✅ `psql --version` shows PostgreSQL version
2. ✅ `python test_postgresql_connection.py` passes all tests
3. ✅ `python view_postgresql_data.py` shows your data
4. ✅ `python run.py` starts your website with PostgreSQL

## 📞 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Verify PostgreSQL installation
3. Check the .env file exists and has correct DATABASE_URL
4. Run the test scripts to identify specific issues

Your Flavi Dairy Forecasting AI will be running on PostgreSQL! 🚀 