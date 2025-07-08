import os
import click
from app import create_app, db
from flask_migrate import Migrate
from app.models.sku import SKU
from app.models.sales import Sales
from app.models.inventory import Inventory
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd
import logging
from app.models.user import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variables (only if not already set)
if not os.environ.get('FLASK_APP'):
    os.environ['FLASK_APP'] = 'run'
if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'development'
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'flavi-dairy-solutions-secret-key-2024'

# Database URL will be loaded from config.py which checks for DATABASE_URL environment variable
# If DATABASE_URL is not set, it defaults to SQLite

# Create Flask app
app = create_app()
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables and sample data."""
    try:
        db.drop_all()
        db.create_all()
        click.echo("Initialized the database.")

        # Create sample SKUs
        skus_data = [
            {'sku_code': 'MILK-1L', 'name': 'Full Cream Milk 1L Pouch', 'category': 'Milk', 'unit_price': 50.0, 'storage_requirement_cubic_meters': 0.001, 'min_threshold': 100},
            {'sku_code': 'CURD-500G', 'name': 'Curd 500g Cup', 'category': 'Curd', 'unit_price': 30.0, 'storage_requirement_cubic_meters': 0.0005, 'min_threshold': 50},
            {'sku_code': 'BUTTER-100G', 'name': 'Butter 100g Pack', 'category': 'Butter', 'unit_price': 80.0, 'storage_requirement_cubic_meters': 0.0002, 'min_threshold': 25},
            {'sku_code': 'YOGURT-200G', 'name': 'Strawberry Yogurt 200g Cup', 'category': 'Yogurt', 'unit_price': 40.0, 'storage_requirement_cubic_meters': 0.0003, 'min_threshold': 75},
            {'sku_code': 'GHEE-500ML', 'name': 'Pure Ghee 500ml Jar', 'category': 'Ghee', 'unit_price': 200.0, 'storage_requirement_cubic_meters': 0.0006, 'min_threshold': 20}
        ]
        for sku_data in skus_data:
            db.session.add(SKU(**sku_data))
        db.session.commit()
        click.echo("Added sample SKUs.")

        # Create admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@flavi.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            click.echo("Created admin user.")

        # Generate sample sales data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        dates = pd.date_range(start_date, end_date, freq='D')

        for sku in SKU.query.all():
            base_demand = {'MILK-1L': 1000, 'CURD-500G': 500, 'BUTTER-100G': 200, 'YOGURT-200G': 300, 'GHEE-500ML': 150}[sku.sku_code]
            for date in dates:
                seasonality = 1 + 0.2 * np.sin(2 * np.pi * (date.month - 1) / 12)
                weekly_pattern = 1.2 if date.weekday() >= 5 else 1.0
                noise = np.random.normal(1, 0.1)
                quantity = int(base_demand * seasonality * weekly_pattern * noise)
                sale = Sales(
                    sku_id=sku.id,
                    date=date.date(),
                    quantity=quantity,
                    revenue=quantity * sku.unit_price
                )
                db.session.add(sale)
        db.session.commit()
        click.echo("Added sample sales data.")

        # Generate sample inventory data
        for sku in SKU.query.all():
            current_level = random.uniform(500, 2000)
            for date in dates:
                inventory = Inventory(
                    sku_id=sku.id,
                    date=date.date(),
                    quantity=int(current_level)
                )
                db.session.add(inventory)
                current_level = max(0, current_level + random.uniform(-200, 200))
        db.session.commit()
        click.echo("Added sample inventory data.")
        
        click.echo("Database initialization complete.")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to initialize database: {e}")
        click.echo(f"Failed to initialize database: {e}")
        raise

if __name__ == '__main__':
    # To initialize the database, run from your terminal:
    # flask init-db
    #
    # Then, to run the application:
    # python run.py
    app.run(debug=True, host='127.0.0.1', port=5000)