#!/usr/bin/env python3
"""
Test script to check orders in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.order import Order
from app.models.customer import Customer
from app.models.sku import SKU

def test_orders():
    app = create_app()
    with app.app_context():
        print("=== Database Order Check ===")
        
        # Check total orders
        total_orders = Order.query.count()
        print(f"Total orders in database: {total_orders}")
        
        # Check customers
        total_customers = Customer.query.count()
        print(f"Total customers in database: {total_customers}")
        
        # Check SKUs
        total_skus = SKU.query.count()
        print(f"Total SKUs in database: {total_skus}")
        
        # List all orders
        if total_orders > 0:
            print("\n=== All Orders ===")
            orders = Order.query.all()
            for order in orders:
                customer = Customer.query.get(order.customer_id)
                sku = SKU.query.filter_by(sku_id=order.sku_id).first()
                print(f"Order ID: {order.id}, Customer: {customer.username if customer else order.customer_id}, SKU: {sku.name if sku else order.sku_id}, Quantity: {order.quantity}, Status: {order.status}, Date: {order.created_at}")
        
        # List all customers
        if total_customers > 0:
            print("\n=== All Customers ===")
            customers = Customer.query.all()
            for customer in customers:
                customer_orders = Order.query.filter_by(customer_id=customer.id).count()
                print(f"Customer ID: {customer.id}, Username: {customer.username}, Email: {customer.email}, Orders: {customer_orders}")

if __name__ == "__main__":
    test_orders() 