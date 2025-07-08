#!/usr/bin/env python3
"""
Database Viewer Script for Flavi Dairy Forecasting AI
This script allows you to view the contents of your database.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def view_database():
    """View the database contents."""
    db_path = 'instance/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return
    
    print(f"🗄️  Database Location: {os.path.abspath(db_path)}")
    print(f"📊 Database Size: {os.path.getsize(db_path) / 1024:.2f} KB")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Tables in database:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # Get row count for each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"    Records: {count}")
            
            # Show sample data for each table
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                sample_data = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                print(f"    Columns: {', '.join(columns)}")
                print("    Sample data:")
                for row in sample_data:
                    print(f"      {row}")
            print()
        
        # Show detailed information for specific tables
        print("🔍 Detailed Information:")
        print("-" * 40)
        
        # Users table
        if any('user' in table[0].lower() for table in tables):
            print("\n👥 Users:")
            try:
                cursor.execute("SELECT username, email, role FROM user LIMIT 5")
                users = cursor.fetchall()
                for user in users:
                    print(f"  {user[0]} ({user[1]}) - {user[2]}")
            except Exception as e:
                print(f"  Error reading users: {e}")
        
        # Customers table
        if any('customer' in table[0].lower() for table in tables):
            print("\n👤 Customers:")
            try:
                cursor.execute("SELECT username, email FROM customer LIMIT 5")
                customers = cursor.fetchall()
                for customer in customers:
                    print(f"  {customer[0]} ({customer[1]})")
            except Exception as e:
                print(f"  Error reading customers: {e}")
        
        # SKUs table
        if any('sku' in table[0].lower() for table in tables):
            print("\n🏷️  SKUs:")
            try:
                cursor.execute("SELECT sku_id, name, category FROM sku LIMIT 5")
                skus = cursor.fetchall()
                for sku in skus:
                    print(f"  {sku[0]} - {sku[1]} ({sku[2]})")
            except Exception as e:
                print(f"  Error reading SKUs: {e}")
        
        # Sales table
        if any('sales' in table[0].lower() for table in tables):
            print("\n💰 Recent Sales:")
            try:
                # First check what columns exist in sales table
                cursor.execute("PRAGMA table_info(sales)")
                sales_columns = [col[1] for col in cursor.fetchall()]
                print(f"  Sales table columns: {sales_columns}")
                
                if 'amount' in sales_columns:
                    cursor.execute("SELECT sku_id, quantity_sold, amount, date FROM sales ORDER BY date DESC LIMIT 5")
                else:
                    cursor.execute("SELECT sku_id, quantity_sold, date FROM sales ORDER BY date DESC LIMIT 5")
                
                sales = cursor.fetchall()
                for sale in sales:
                    if len(sale) == 4:
                        print(f"  {sale[0]} - Qty: {sale[1]}, Amount: ₹{sale[2]:.2f}, Date: {sale[3]}")
                    else:
                        print(f"  {sale[0]} - Qty: {sale[1]}, Date: {sale[2]}")
            except Exception as e:
                print(f"  Error reading sales: {e}")
        
        # Inventory table
        if any('inventory' in table[0].lower() for table in tables):
            print("\n📦 Recent Inventory:")
            try:
                cursor.execute("SELECT sku_id, current_level, date FROM inventory ORDER BY date DESC LIMIT 5")
                inventory = cursor.fetchall()
                for inv in inventory:
                    print(f"  {inv[0]} - Level: {inv[1]:.2f}, Date: {inv[2]}")
            except Exception as e:
                print(f"  Error reading inventory: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {str(e)}")

if __name__ == '__main__':
    view_database() 