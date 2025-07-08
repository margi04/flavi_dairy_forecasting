#!/usr/bin/env python3
"""
Simple database viewer for Flavi Dairy Forecasting AI
"""

import sqlite3
import os
from datetime import datetime

def show_database():
    db_path = 'instance/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    # Get file size
    file_size = os.path.getsize(db_path)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"🗄️  Database: {db_path}")
    print(f"📊 Size: {file_size_mb:.2f} MB")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 Found {len(tables)} tables:")
        print()
        
        for table in tables:
            table_name = table[0]
            print(f"🔹 Table: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"   Columns: {len(columns)}")
            for col in columns:
                col_name, col_type = col[1], col[2]
                print(f"     - {col_name} ({col_type})")
            
            # Get record count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   Records: {count}")
            
            # Show sample data
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                sample_data = cursor.fetchall()
                print(f"   Sample data:")
                for i, row in enumerate(sample_data, 1):
                    print(f"     {i}. {row}")
            
            print()
        
        # Show some specific data
        print("📊 Detailed Data Summary:")
        print("-" * 40)
        
        # Users
        cursor.execute("SELECT COUNT(*) FROM user;")
        user_count = cursor.fetchone()[0]
        print(f"👥 Users: {user_count}")
        
        # Customers
        cursor.execute("SELECT COUNT(*) FROM customer;")
        customer_count = cursor.fetchone()[0]
        print(f"👤 Customers: {customer_count}")
        
        # SKUs
        cursor.execute("SELECT COUNT(*) FROM sku;")
        sku_count = cursor.fetchone()[0]
        print(f"📦 SKUs: {sku_count}")
        
        # Orders
        cursor.execute("SELECT COUNT(*) FROM 'order';")
        order_count = cursor.fetchone()[0]
        print(f"📋 Orders: {order_count}")
        
        # Sales
        cursor.execute("SELECT COUNT(*) FROM sales;")
        sales_count = cursor.fetchone()[0]
        print(f"💰 Sales Records: {sales_count}")
        
        # Inventory
        cursor.execute("SELECT COUNT(*) FROM inventory;")
        inventory_count = cursor.fetchone()[0]
        print(f"📦 Inventory Records: {inventory_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {str(e)}")

if __name__ == "__main__":
    show_database() 