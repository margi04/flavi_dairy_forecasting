#!/usr/bin/env python3
"""
Script to add role column to existing customer table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def add_role_column():
    app = create_app()
    with app.app_context():
        print("=== Adding role column to customer table ===")
        
        try:
            # Add role column to customer table
            db.session.execute(text("ALTER TABLE customer ADD COLUMN role VARCHAR(16) DEFAULT 'customer'"))
            db.session.commit()
            print("✅ Role column added successfully to customer table")
            
            # Update existing customers to have 'customer' role
            db.session.execute(text("UPDATE customer SET role = 'customer' WHERE role IS NULL"))
            db.session.commit()
            print("✅ Updated existing customers with 'customer' role")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_role_column() 