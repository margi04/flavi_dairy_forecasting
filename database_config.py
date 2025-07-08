#!/usr/bin/env python3
"""
Database Configuration for Flavi Dairy Forecasting AI
Handles database connections, migrations, and configuration for both SQLite and PostgreSQL.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, app=None):
        self.app = app
        self.db = None
        self.migrate = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the database with the Flask app."""
        self.app = app
        
        # Use existing SQLAlchemy instance if available
        if hasattr(app, 'extensions') and 'sqlalchemy' in app.extensions:
            self.db = app.extensions['sqlalchemy'].db
            logger.info("Using existing SQLAlchemy instance")
        else:
            # Configure database URI
            self._configure_database_uri(app)
            
            # Initialize SQLAlchemy and Migrate
            self.db = SQLAlchemy(app)
            self.migrate = Migrate(app, self.db)
            
            # Test database connection
            self._test_connection()
    
    def _configure_database_uri(self, app):
        """Configure the database URI based on environment."""
        # Check for PostgreSQL configuration
        if os.environ.get('DATABASE_URL'):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
            logger.info("Using PostgreSQL database")
        else:
            # Use SQLite for development
            basedir = os.path.abspath(os.path.dirname(__file__))
            db_path = os.path.join(basedir, 'instance', 'flavi_dairy_forecasting_ai.sqlite')
            
            # Ensure instance directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            logger.info(f"Using SQLite database: {db_path}")
        
        # Common SQLAlchemy settings
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
    
    def _test_connection(self):
        """Test the database connection."""
        try:
            with self.app.app_context():
                # Test basic connection
                result = self.db.session.execute(text('SELECT 1'))
                result.fetchone()
                logger.info("✅ Database connection successful")
                
                # Check if tables exist
                self._check_tables()
                
        except SQLAlchemyError as e:
            logger.error(f"❌ Database connection failed: {str(e)}")
            raise
    
    def _check_tables(self):
        """Check if required tables exist."""
        try:
            # Import models to check if tables exist
            from app.models.user import User
            from app.models.customer import Customer
            from app.models.sku import SKU
            from app.models.sales import Sales
            from app.models.inventory import Inventory
            
            # Try to query each table
            tables = [User, Customer, SKU, Sales, Inventory]
            existing_tables = []
            
            for table in tables:
                try:
                    table.query.first()
                    existing_tables.append(table.__tablename__)
                except Exception:
                    pass
            
            if existing_tables:
                logger.info(f"📋 Existing tables: {', '.join(existing_tables)}")
            else:
                logger.warning("⚠️  No tables found. Run database initialization.")
                
        except Exception as e:
            logger.warning(f"⚠️  Could not check tables: {str(e)}")
    
    def create_tables(self):
        """Create all database tables."""
        try:
            with self.app.app_context():
                self.db.create_all()
                logger.info("✅ All database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)."""
        try:
            with self.app.app_context():
                self.db.drop_all()
                logger.info("🗑️  All database tables dropped")
        except Exception as e:
            logger.error(f"❌ Error dropping tables: {str(e)}")
            raise
    
    def get_connection_info(self):
        """Get database connection information."""
        try:
            with self.app.app_context():
                engine = self.db.engine
                url = engine.url
                
                info = {
                    'database_type': url.drivername,
                    'host': getattr(url, 'host', 'N/A'),
                    'port': getattr(url, 'port', 'N/A'),
                    'database': getattr(url, 'database', 'N/A'),
                    'username': getattr(url, 'username', 'N/A'),
                }
                
                return info
        except Exception as e:
            logger.error(f"❌ Error getting connection info: {str(e)}")
            return None
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database."""
        try:
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f'backup_{timestamp}.sql'
            
            with self.app.app_context():
                engine = self.db.engine
                
                if engine.url.drivername == 'sqlite':
                    # SQLite backup
                    import shutil
                    shutil.copy2(engine.url.database, backup_path)
                    logger.info(f"✅ SQLite backup created: {backup_path}")
                else:
                    # PostgreSQL backup
                    import subprocess
                    cmd = f'pg_dump {engine.url} > {backup_path}'
                    subprocess.run(cmd, shell=True, check=True)
                    logger.info(f"✅ PostgreSQL backup created: {backup_path}")
                    
        except Exception as e:
            logger.error(f"❌ Error creating backup: {str(e)}")
            raise
    
    def restore_database(self, backup_path):
        """Restore database from backup."""
        try:
            with self.app.app_context():
                engine = self.db.engine
                
                if engine.url.drivername == 'sqlite':
                    # SQLite restore
                    import shutil
                    shutil.copy2(backup_path, engine.url.database)
                    logger.info(f"✅ SQLite restored from: {backup_path}")
                else:
                    # PostgreSQL restore
                    import subprocess
                    cmd = f'psql {engine.url} < {backup_path}'
                    subprocess.run(cmd, shell=True, check=True)
                    logger.info(f"✅ PostgreSQL restored from: {backup_path}")
                    
        except Exception as e:
            logger.error(f"❌ Error restoring backup: {str(e)}")
            raise

# Global database manager instance
db_manager = DatabaseManager()

def get_db():
    """Get the database instance."""
    return db_manager.db

def get_migrate():
    """Get the migrate instance."""
    return db_manager.migrate

def init_database_manager(app):
    """Initialize the database manager with the Flask app."""
    db_manager.init_app(app)
    return db_manager

if __name__ == '__main__':
    # Test database configuration
    from app import create_app
    
    app = create_app()
    db_manager = init_database_manager(app)
    
    print("🔍 Database Configuration Test")
    print("=" * 40)
    
    # Get connection info
    info = db_manager.get_connection_info()
    if info:
        print(f"Database Type: {info['database_type']}")
        print(f"Host: {info['host']}")
        print(f"Port: {info['port']}")
        print(f"Database: {info['database']}")
        print(f"Username: {info['username']}")
    
    print("\n✅ Database configuration test completed!") 