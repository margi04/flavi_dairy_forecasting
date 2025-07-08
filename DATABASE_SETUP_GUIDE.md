 # Database Setup Guide for Flavi Dairy Forecasting AI

This guide explains how to set up and manage the database for the Flavi Dairy Forecasting AI system.

## 🗄️ Database Overview

The system supports both SQLite (development) and PostgreSQL (production) databases with the following tables:

- **Users** - Admin users with authentication
- **Customers** - Customer accounts with authentication
- **SKUs** - Product catalog with detailed specifications
- **Sales** - Sales transactions linked to customers and SKUs
- **Inventory** - Inventory levels and management data

## 🚀 Quick Start

### 1. Automatic Setup (Recommended)

Run the comprehensive setup script:

```bash
python setup_database.py
```

This will:
- Create all database tables
- Add sample data (admin users, customers, SKUs, inventory, sales)
- Display login credentials

### 2. Manual Setup

If you prefer manual setup:

```bash
# Create tables only
python setup_database.py --no-seed

# Force setup (overwrite existing data)
python setup_database.py --force

# Reset database (drop all tables and recreate)
python setup_database.py --reset

# Show database information
python setup_database.py --info
```

## 🔧 Database Configuration

### SQLite (Development - Default)

The system automatically uses SQLite for development. The database file is stored at:
```
instance/flavi_dairy_forecasting_ai.sqlite
```

### PostgreSQL (Production)

To use PostgreSQL, set the environment variable:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/flavi_dairy"
```

Or create a `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/flavi_dairy
```

## 📊 Sample Data

The setup script creates the following sample data:

### Admin Users
- **admin** / admin123
- **manager** / manager123

### Customers
- **customer1** / customer123
- **customer2** / customer123
- **customer3** / customer123
- **customer4** / customer123
- **customer5** / customer123

### SKUs (Products)
- Full Cream Milk 1L
- Toned Milk 1L
- Fresh Curd 500g
- Unsalted Butter 250g
- Cheddar Cheese 200g
- Pure Ghee 1L

### Sample Data
- 30 days of inventory records
- 90 days of sales transactions
- Realistic data with proper relationships

## 🔄 Database Operations

### Registration Forms

The system handles data storage for all registration forms:

#### Customer Registration (`/customer_register`)
- Stores data in the `Customer` table
- Validates unique username/email across both User and Customer tables
- Password hashing for security
- Automatic timestamp creation

#### Admin Registration (`/admin_register`)
- Stores data in the `User` table with role='admin'
- Validates unique username/email across both tables
- Password hashing for security

#### SKU Management (`/skus_page`)
- **Add SKU**: Creates new SKU records with full validation
- **Edit SKU**: Updates existing SKU data with validation
- **Delete SKU**: Removes SKU (with relationship checks)
- **Search & Export**: Full CRUD with search and export functionality

#### Inventory Management (`/inventory`)
- **Add Inventory**: Creates inventory records linked to SKUs
- **Edit Inventory**: Updates inventory levels and details
- **Delete Inventory**: Removes inventory records
- **Low Stock Alerts**: Automatic threshold monitoring

### API Endpoints

All database operations are available via RESTful API endpoints:

```bash
# SKU Management
POST /add_sku          # Create new SKU
POST /edit_sku         # Update existing SKU
POST /delete_sku       # Delete SKU

# Inventory Management
POST /add_inventory    # Create inventory record
POST /edit_inventory/<id>  # Update inventory
POST /delete_inventory/<id> # Delete inventory

# Data Retrieval
GET /api/skus          # Get all SKUs
GET /api/sales/<sku_id> # Get sales for SKU
GET /api/inventory/<sku_id> # Get inventory for SKU
```

## 🛡️ Data Validation

All database operations include comprehensive validation:

### Input Validation
- Required field checking
- Data type validation
- Email format validation
- Password strength requirements
- Numeric value validation

### Business Logic Validation
- Unique constraint checking
- Foreign key relationship validation
- Data integrity checks
- Relationship dependency validation

### Error Handling
- Database transaction rollback on errors
- User-friendly error messages
- Proper HTTP status codes
- Logging for debugging

## 🔍 Database Monitoring

### Connection Testing
The system automatically tests database connections on startup:

```python
# Automatic connection test
with app.app_context():
    result = db.session.execute(text('SELECT 1'))
    result.fetchone()
```

### Health Checks
Monitor database health with:

```bash
python setup_database.py --info
```

This shows:
- Database connection details
- Table counts
- Data summary

## 📈 Data Analytics

The system provides built-in analytics:

### Dashboard Metrics
- Total sales amount
- Total orders count
- Active SKUs count
- Customer count

### Charts and Visualizations
- Sales trend charts
- Product distribution pie charts
- Inventory level monitoring
- Low stock alerts

### Export Functionality
- CSV export for all data
- Filtered data export
- Date range selection
- Custom field selection

## 🔐 Security Features

### Password Security
- Bcrypt hashing for all passwords
- Salt generation for security
- Password strength validation

### User Authentication
- Session-based authentication
- Role-based access control
- Login/logout functionality
- Password reset capability

### Data Protection
- SQL injection prevention
- Input sanitization
- CSRF protection
- Secure session management

## 🚨 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check database file permissions
ls -la instance/flavi_dairy_forecasting_ai.sqlite

# Recreate database
python setup_database.py --reset
```

#### Migration Issues
```bash
# Reset migrations
flask db stamp head
flask db migrate
flask db upgrade
```

#### Data Corruption
```bash
# Backup current data
cp instance/flavi_dairy_forecasting_ai.sqlite backup.sqlite

# Reset and recreate
python setup_database.py --reset
```

### Logs and Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check application logs for database errors and connection issues.

## 📚 Additional Resources

### Database Schema
See individual model files for complete schema:
- `app/models/user.py`
- `app/models/customer.py`
- `app/models/sku.py`
- `app/models/sales.py`
- `app/models/inventory.py`

### Configuration
- `config.py` - Main configuration
- `database_config.py` - Database-specific configuration

### Scripts
- `setup_database.py` - Main setup script
- `init_db.py` - Legacy initialization script
- `database_config.py` - Database manager

## 🎯 Best Practices

1. **Always backup before major changes**
2. **Use transactions for data integrity**
3. **Validate all user inputs**
4. **Monitor database performance**
5. **Regular data backups**
6. **Test migrations in development first**

## 📞 Support

For database-related issues:
1. Check the logs for error messages
2. Verify database file permissions
3. Test database connection
4. Review configuration settings
5. Consult this guide for common solutions

---

**Note**: This system is designed for dairy product forecasting and inventory management. All data is stored securely with proper validation and error handling.