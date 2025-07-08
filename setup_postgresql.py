#!/usr/bin/env python3
"""
PostgreSQL Setup and Migration Script for Flavi Dairy Forecasting AI
This script helps set up PostgreSQL database and migrate data from SQLite.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlite3
from datetime import datetime
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_postgresql_database():
    """Create PostgreSQL database and user."""
    print("🐘 Setting up PostgreSQL database...")
    
    # PostgreSQL connection parameters
    host = input("Enter PostgreSQL host (default: localhost): ").strip() or "localhost"
    port = input("Enter PostgreSQL port (default: 5432): ").strip() or "5432"
    admin_user = input("Enter PostgreSQL admin username (default: postgres): ").strip() or "postgres"
    admin_password = input("Enter PostgreSQL admin password: ").strip()
    
    if not admin_password:
        print("❌ Admin password is required!")
        return False
    
    try:
        # Connect to PostgreSQL as admin
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create database and user
        db_name = "flavi_dairy_forecasting"
        db_user = "flavi_user"
        db_password = "flavi_password_2024"
        
        print(f"📝 Creating database: {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        
        print(f"👤 Creating user: {db_user}")
        cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        
        cursor.close()
        conn.close()
        
        # Test connection with new user
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        test_conn.close()
        
        print("✅ PostgreSQL database setup successful!")
        
        # Save connection details to .env file
        env_content = f"""# PostgreSQL Database Configuration
DATABASE_URL=postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}

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
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("📄 Created .env file with database configuration")
        print(f"🔗 Database URL: postgresql://{db_user}:***@{host}:{port}/{db_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up PostgreSQL: {str(e)}")
        return False

def migrate_data_from_sqlite():
    """Migrate data from SQLite to PostgreSQL."""
    print("\n🔄 Migrating data from SQLite to PostgreSQL...")
    
    sqlite_path = 'instance/app.db'
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite database not found at: {sqlite_path}")
        return False
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to PostgreSQL
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return False
        
        pg_conn = psycopg2.connect(database_url)
        pg_cursor = pg_conn.cursor()
        
        # Get all tables from SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = sqlite_cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"📋 Migrating table: {table_name}")
            
            # Get table schema
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = sqlite_cursor.fetchall()
            
            # Create table in PostgreSQL
            column_definitions = []
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                col_not_null = "NOT NULL" if col[3] else ""
                col_default = f"DEFAULT {col[4]}" if col[4] else ""
                
                # Convert SQLite types to PostgreSQL types
                if col_type.upper() == 'INTEGER':
                    pg_type = 'INTEGER'
                elif col_type.upper() == 'TEXT':
                    pg_type = 'TEXT'
                elif col_type.upper() == 'REAL':
                    pg_type = 'DOUBLE PRECISION'
                elif col_type.upper() == 'BLOB':
                    pg_type = 'BYTEA'
                else:
                    pg_type = 'TEXT'
                
                column_definitions.append(f"{col_name} {pg_type} {col_not_null} {col_default}".strip())
            
            # Create table
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
            pg_cursor.execute(create_table_sql)
            
            # Migrate data
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                # Get column names
                column_names = [col[1] for col in columns]
                placeholders = ', '.join(['%s'] * len(column_names))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
                
                pg_cursor.executemany(insert_sql, rows)
                print(f"  ✅ Migrated {len(rows)} rows")
            else:
                print(f"  ℹ️  No data to migrate")
        
        pg_conn.commit()
        sqlite_conn.close()
        pg_conn.close()
        
        print("✅ Data migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error migrating data: {str(e)}")
        return False

def setup_flask_migrations():
    """Set up Flask-Migrate for PostgreSQL."""
    print("\n🔧 Setting up Flask-Migrate...")
    
    try:
        # Set environment variables
        os.environ['FLASK_APP'] = 'run.py'
        
        # Initialize migrations
        os.system('flask db init')
        os.system('flask db migrate -m "Initial migration"')
        os.system('flask db upgrade')
        
        print("✅ Flask-Migrate setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Flask-Migrate: {str(e)}")
        return False

def main():
    """Main function to run the setup."""
    print("🚀 Flavi Dairy Forecasting AI - PostgreSQL Setup")
    print("=" * 50)
    
    # Step 1: Create PostgreSQL database
    if not create_postgresql_database():
        print("❌ Failed to create PostgreSQL database")
        return
    
    # Step 2: Migrate data
    if not migrate_data_from_sqlite():
        print("❌ Failed to migrate data")
        return
    
    # Step 3: Setup Flask-Migrate
    if not setup_flask_migrations():
        print("❌ Failed to setup Flask-Migrate")
        return
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with the correct DATABASE_URL")
    print("2. Run 'python run.py' to start your application")
    print("3. Your website will now use PostgreSQL instead of SQLite")

if __name__ == '__main__':
    main() 