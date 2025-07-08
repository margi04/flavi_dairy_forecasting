# How to View PostgreSQL Data - Complete Guide

There are several ways to view your PostgreSQL data. Here are all the methods:

## 🚀 Method 1: Interactive Data Viewer (Recommended)

Run the interactive viewer script:

```bash
python view_postgresql_data.py
```

This gives you a menu with options to:
- View all tables overview
- View users, customers, SKUs, sales, inventory
- View specific table data
- Export data to CSV
- View everything at once

## 📊 Method 2: Quick Database Overview

View basic database information:

```bash
python view_postgresql_database.py
```

This shows:
- Database connection info
- All tables and record counts
- Sample data from each table
- Database statistics

## 🔍 Method 3: Test Connection and Data Integrity

Test your PostgreSQL setup:

```bash
python test_postgresql_connection.py
```

This verifies:
- Database connection
- Flask-SQLAlchemy integration
- Data integrity after migration

## 🖥️ Method 4: Using pgAdmin 4 (GUI Tool)

If you installed pgAdmin 4:

1. **Open pgAdmin 4**
2. **Connect to your database:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `flavi_dairy_forecasting`
   - Username: `flavi_user`
   - Password: `flavi_password_2024`

3. **Navigate to your data:**
   - Expand: `Servers` → `PostgreSQL` → `Databases` → `flavi_dairy_forecasting` → `Schemas` → `public` → `Tables`

4. **View table data:**
   - Right-click any table → "View/Edit Data" → "All Rows"

## 💻 Method 5: Using psql Command Line

Connect directly to PostgreSQL:

```bash
psql -U flavi_user -d flavi_dairy_forecasting
```

### Useful psql Commands:

```sql
-- List all tables
\dt

-- View table structure
\d table_name

-- View all data from a table
SELECT * FROM table_name;

-- View specific columns
SELECT username, email FROM "user";

-- Count records
SELECT COUNT(*) FROM table_name;

-- View recent sales
SELECT * FROM sales ORDER BY date DESC LIMIT 10;

-- View users
SELECT username, email, role FROM "user";

-- View customers
SELECT username, email FROM customer;

-- View SKUs
SELECT sku_id, name, category, unit_price FROM sku;

-- View inventory
SELECT * FROM inventory ORDER BY date DESC LIMIT 10;

-- Exit psql
\q
```

## 🌐 Method 6: Through Your Website

Your Flask application already displays data through the web interface:

1. **Start your application:**
   ```bash
   python run.py
   ```

2. **Open your browser:**
   - Go to `http://localhost:5000`
   - Login with your credentials
   - Navigate to different sections to view data

3. **Available pages:**
   - Dashboard: Overview of data
   - Users: View all users
   - Customers: View all customers
   - SKUs: View all products
   - Sales: View sales data
   - Inventory: View inventory levels

## 📄 Method 7: Export to CSV

Export any table to CSV for analysis:

```bash
python view_postgresql_data.py
# Choose option 8: Export table to CSV
# Enter the table name you want to export
```

Or use the direct export function:

```python
from view_postgresql_data import export_to_csv
export_to_csv('user')  # Exports user table
export_to_csv('sales')  # Exports sales table
```

## 🔧 Method 8: Using Python Scripts

Create custom scripts to view specific data:

```python
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(database_url)
cursor = conn.cursor()

# View all users
cursor.execute("SELECT username, email FROM \"user\"")
users = cursor.fetchall()
for user in users:
    print(f"User: {user[0]}, Email: {user[1]}")

conn.close()
```

## 📊 Method 9: Using Pandas for Analysis

For data analysis:

```python
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.environ.get('DATABASE_URL')

# Load data into pandas
users_df = pd.read_sql_query("SELECT * FROM \"user\"", database_url)
sales_df = pd.read_sql_query("SELECT * FROM sales", database_url)
inventory_df = pd.read_sql_query("SELECT * FROM inventory", database_url)

# View data
print(users_df.head())
print(sales_df.describe())
```

## 🎯 Quick Commands Summary

### View All Data at Once:
```bash
python view_postgresql_data.py
# Choose option 9: View everything
```

### View Specific Tables:
```bash
# Users
python -c "from view_postgresql_data import view_users; view_users()"

# Sales
python -c "from view_postgresql_data import view_recent_sales; view_recent_sales()"

# Inventory
python -c "from view_postgresql_data import view_inventory; view_inventory()"
```

### Export Data:
```bash
python -c "from view_postgresql_data import export_to_csv; export_to_csv('sales')"
```

## 🔍 Troubleshooting

### If you can't connect:
1. Make sure PostgreSQL is running
2. Check your `.env` file has correct `DATABASE_URL`
3. Verify the database exists
4. Test connection: `python test_postgresql_connection.py`

### If tables are empty:
1. Check if migration was successful
2. Run: `python migrate_to_postgresql.py`
3. Verify with: `python view_postgresql_database.py`

### If you get permission errors:
1. Make sure the user has proper permissions
2. Check the database URL format
3. Verify the user exists in PostgreSQL

## 📈 Data Visualization

For charts and graphs, you can:

1. **Export to CSV** and use Excel/Google Sheets
2. **Use pandas** with matplotlib/plotly
3. **Use your website's built-in charts** (if available)
4. **Connect to BI tools** like Tableau or Power BI

## 🎉 Success!

Once you can view your data, you'll see:
- ✅ All your users and customers
- ✅ Product catalog (SKUs)
- ✅ Sales history
- ✅ Inventory levels
- ✅ All data safely stored in PostgreSQL

Your Flavi Dairy Forecasting AI data is now accessible through multiple methods! 🚀 