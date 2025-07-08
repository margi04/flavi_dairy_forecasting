#!/usr/bin/env python3
"""
Script to add recent test orders for debugging
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.order import Order
from app.models.customer import Customer
from app.models.sku import SKU
from datetime import datetime, timedelta

def add_recent_orders():
    app = create_app()
    with app.app_context():
        print("=== Adding Recent Test Orders ===")
        
        # Get a customer
        customer = Customer.query.first()
        if not customer:
            print("No customers found in database")
            return
        
        # Get all SKUs
        skus = SKU.query.all()
        if not skus:
            print("No SKUs found in database")
            return
        
        print(f"Adding orders for customer: {customer.username}")
        
        # Add orders for the last 3 days
        for i in range(3):
            date = datetime.now() - timedelta(days=i)
            for sku in skus:
                order = Order(
                    customer_id=customer.id,
                    sku_id=sku.sku_id,
                    quantity=i + 1,
                    status='pending' if i == 0 else 'completed',
                    created_at=date
                )
                db.session.add(order)
                print(f"Added order: {sku.name} - Quantity: {i + 1} - Date: {date.strftime('%Y-%m-%d %H:%M')}")
        
        db.session.commit()
        print("Recent test orders added successfully!")

if __name__ == "__main__":
    add_recent_orders() 