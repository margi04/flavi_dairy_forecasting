# PostgreSQL Setup Guide for Flavi Dairy Solutions

This guide will help you migrate from SQLite to PostgreSQL and set up pgAdmin 4 for better data management.

## Prerequisites

1. **PostgreSQL Server** - Download and install from [postgresql.org](https://www.postgresql.org/download/)
2. **pgAdmin 4** - Download and install from [pgadmin.org](https://www.pgadmin.org/download/)
3. **Python dependencies** - Already included in requirements.txt

## Step 1: Install PostgreSQL

### Windows:
1. Download PostgreSQL installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Choose installation directory
4. Set a password for the `postgres` user (remember this!)
5. Keep default port (5432)
6. Complete installation

### macOS:
```bash
brew install postgresql
brew services start postgresql
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 2: Install pgAdmin 4

1. Download pgAdmin 4 from [pgadmin.org](https://www.pgadmin.org/download/)
2. Install and launch pgAdmin 4
3. Set up a master password when prompted
4. Connect to your PostgreSQL server

## Step 3: Create Database in pgAdmin 4

1. Open pgAdmin 4
2. Right-click on "Databases" → "Create" → "Database"
3. Name: `flavi_dairy_db`
4. Click "Save"

## Step 4: Setup PostgreSQL Connection

Run the setup script to configure your database connection:

```bash
python setup_postgresql.py
```

This script will:
- Ask for your PostgreSQL connection details
- Test the connection
- Create a `.env` file with your configuration
- Create database tables
- Set up the default admin user

## Step 5: Migrate Existing Data (Optional)

If you have existing data in SQLite, migrate it to PostgreSQL:

```bash
python migrate_to_postgresql.py
```

This will copy all your existing users, customers, SKUs, sales, and inventory data.

## Step 6: Run Your Application

```bash
python run.py
```

Your application will now use PostgreSQL instead of SQLite!

## Database Schema

Your PostgreSQL database will contain these tables:

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `role` (admin/user)

### Customers Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`

### SKUs Table
- `id` (Primary Key)
- `sku_code` (Unique)
- `name`
- `category`
- `unit_price`
- `storage_requirement_cubic_meters`
- `min_threshold`
- `created_at`

### Sales Table
- `id` (Primary Key)
- `sku_id` (Foreign Key)
- `date`
- `quantity`
- `revenue`

### Inventory Table
- `id` (Primary Key)
- `sku_id` (Foreign Key)
- `date`
- `quantity`

## Viewing Data in pgAdmin 4

1. Open pgAdmin 4
2. Connect to your PostgreSQL server
3. Navigate to: `Servers` → `PostgreSQL` → `Databases` → `flavi_dairy_db` → `Schemas` → `public` → `Tables`
4. Right-click any table → "View/Edit Data" → "All Rows"

## Environment Variables

The setup creates a `.env` file with:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=flavi-dairy-solutions-secret-key-2024

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/flavi_dairy_db

# PostgreSQL Connection Details
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flavi_dairy_db
```

## Troubleshooting

### Connection Issues
- Ensure PostgreSQL service is running
- Check username/password
- Verify database exists
- Check firewall settings

### Permission Issues
- Ensure your user has proper permissions
- Grant necessary privileges in pgAdmin 4

### Migration Issues
- Backup your SQLite database first
- Check for duplicate data
- Verify all tables exist

## Benefits of PostgreSQL

1. **Better Performance** - Handles large datasets efficiently
2. **Advanced Features** - Full-text search, JSON support, etc.
3. **Data Integrity** - ACID compliance, constraints, triggers
4. **Scalability** - Can handle concurrent users and large data volumes
5. **Professional Tooling** - pgAdmin 4 provides excellent data management

## Switching Back to SQLite

If you need to switch back to SQLite for development:

1. Comment out the `DATABASE_URL` in `.env`
2. Or delete the `.env` file
3. The application will automatically use SQLite

## Support

If you encounter issues:
1. Check the PostgreSQL logs
2. Verify connection settings
3. Ensure all dependencies are installed
4. Test connection manually in pgAdmin 4 