#!/usr/bin/env python3
"""
Migration Script: SQLite to PostgreSQL
This script migrates all data from SQLite to PostgreSQL for Flavi Dairy Forecasting AI
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_sqlite_data():
    """Extract all data from SQLite database."""
    print("📊 Extracting data from SQLite...")
    
    sqlite_path = 'instance/app.db'
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite database not found at: {sqlite_path}")
        return None
    
    try:
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row  # This allows column access by name
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        data = {}
        for table in tables:
            table_name = table[0]
            print(f"  📋 Extracting from table: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            # Get all data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            data[table_name] = {
                'columns': [col[1] for col in columns],
                'rows': [dict(row) for row in rows]
            }
            
            print(f"    ✅ Extracted {len(rows)} rows")
        
        conn.close()
        print(f"✅ Extracted data from {len(tables)} tables")
        return data
        
    except Exception as e:
        print(f"❌ Error extracting data: {str(e)}")
        return None

def create_postgresql_tables(data, pg_conn):
    """Create tables in PostgreSQL based on SQLite schema."""
    print("🏗️  Creating PostgreSQL tables...")
    
    cursor = pg_conn.cursor()
    
    for table_name, table_data in data.items():
        print(f"  📋 Creating table: {table_name}")
        
        # Get column definitions
        columns = table_data['columns']
        sample_row = table_data['rows'][0] if table_data['rows'] else {}
        
        # Create column definitions
        column_definitions = []
        for col_name in columns:
            # Determine PostgreSQL data type based on sample data
            if col_name in sample_row:
                value = sample_row[col_name]
                if isinstance(value, int):
                    pg_type = 'INTEGER'
                elif isinstance(value, float):
                    pg_type = 'DOUBLE PRECISION'
                elif isinstance(value, bool):
                    pg_type = 'BOOLEAN'
                elif isinstance(value, datetime):
                    pg_type = 'TIMESTAMP'
                else:
                    pg_type = 'TEXT'
            else:
                pg_type = 'TEXT'
            
            column_definitions.append(f"{col_name} {pg_type}")
        
        # Create table
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(column_definitions)}
        )
        """
        
        try:
            cursor.execute(create_sql)
            print(f"    ✅ Table {table_name} created")
        except Exception as e:
            print(f"    ⚠️  Table {table_name} might already exist: {str(e)}")
    
    pg_conn.commit()
    cursor.close()

def insert_data_to_postgresql(data, pg_conn):
    """Insert data into PostgreSQL tables."""
    print("📥 Inserting data into PostgreSQL...")
    
    cursor = pg_conn.cursor()
    
    for table_name, table_data in data.items():
        if not table_data['rows']:
            print(f"  ℹ️  No data to insert for table: {table_name}")
            continue
        
        print(f"  📋 Inserting data into: {table_name}")
        
        columns = table_data['columns']
        rows = table_data['rows']
        
        # Prepare insert statement
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Prepare data for insertion
        data_to_insert = []
        for row in rows:
            row_data = []
            for col in columns:
                value = row.get(col)
                # Handle None values and data type conversions
                if value is None:
                    row_data.append(None)
                elif isinstance(value, datetime):
                    row_data.append(value.isoformat())
                else:
                    row_data.append(value)
            data_to_insert.append(row_data)
        
        try:
            cursor.executemany(insert_sql, data_to_insert)
            print(f"    ✅ Inserted {len(rows)} rows")
        except Exception as e:
            print(f"    ❌ Error inserting data: {str(e)}")
            # Try inserting row by row to identify problematic data
            for i, row_data in enumerate(data_to_insert):
                try:
                    cursor.execute(insert_sql, row_data)
                except Exception as row_error:
                    print(f"      ❌ Row {i+1} failed: {str(row_error)}")
                    print(f"      Data: {row_data}")
    
    pg_conn.commit()
    cursor.close()

def verify_migration(data, pg_conn):
    """Verify that data was migrated correctly."""
    print("🔍 Verifying migration...")
    
    cursor = pg_conn.cursor()
    
    for table_name, table_data in data.items():
        print(f"  📋 Verifying table: {table_name}")
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        pg_count = cursor.fetchone()[0]
        sqlite_count = len(table_data['rows'])
        
        print(f"    SQLite: {sqlite_count} rows")
        print(f"    PostgreSQL: {pg_count} rows")
        
        if pg_count == sqlite_count:
            print(f"    ✅ Row count matches")
        else:
            print(f"    ❌ Row count mismatch!")
        
        # Show sample data
        if pg_count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            sample = cursor.fetchone()
            print(f"    Sample data: {sample}")
    
    cursor.close()

def main():
    """Main migration function."""
    print("🚀 SQLite to PostgreSQL Migration")
    print("=" * 40)
    
    # Step 1: Extract data from SQLite
    data = get_sqlite_data()
    if not data:
        print("❌ Failed to extract data from SQLite")
        return
    
    # Step 2: Connect to PostgreSQL
    print("\n🔗 Connecting to PostgreSQL...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        print("Please run setup_postgresql.py first")
        return
    
    try:
        pg_conn = psycopg2.connect(database_url)
        print("✅ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {str(e)}")
        return
    
    try:
        # Step 3: Create tables
        create_postgresql_tables(data, pg_conn)
        
        # Step 4: Insert data
        insert_data_to_postgresql(data, pg_conn)
        
        # Step 5: Verify migration
        verify_migration(data, pg_conn)
        
        print("\n🎉 Migration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Your application is now using PostgreSQL")
        print("2. You can safely remove the SQLite database file")
        print("3. Run 'python run.py' to start your application")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
    finally:
        pg_conn.close()

if __name__ == '__main__':
    main() 