# Database Structure: Separate User and Customer Tables

## ✅ **YES, there are separate tables for Users and Customers**

The database has **TWO SEPARATE TABLES** with different purposes:

## 📊 **1. USER TABLE (For Admin Users)**

### Purpose
- Stores **admin users** and some legacy customer data
- Used for **admin login verification**

### Current Data
```
Total Users: 7
- admin (Role: admin)
- customer1 (Role: customer) - Legacy data
- customer2 (Role: customer) - Legacy data  
- Akanksha (Role: admin)
- akanksha (Role: admin)
- riya (Role: admin)
- aditi (Role: admin)
```

### Schema
```sql
User Table:
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- role (admin/customer)
```

### Login Process
```python
# Admin login verification from User table
user = User.query.filter_by(username=username, role='admin').first()
```

## 📊 **2. CUSTOMER TABLE (For Customer Users)**

### Purpose
- Stores **customer users only**
- Used for **customer login verification**

### Current Data
```
Total Customers: 4
- margi (Role: customer)
- piyush (Role: customer)
- riya (Role: customer)
- testcustomer (Role: customer)
```

### Schema
```sql
Customer Table:
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- role (always 'customer')
- created_at (Timestamp)
```

### Login Process
```python
# Customer login verification from Customer table
customer = Customer.query.filter_by(username=username).first()
```

## 🔐 **Login Verification Process**

### Admin Login
1. User clicks "Admin Login" tab
2. System searches **User table** for username with `role='admin'`
3. Verifies password
4. Creates admin session
5. Redirects to admin dashboard

### Customer Login
1. User clicks "Customer Login" tab
2. System searches **Customer table** for username
3. Verifies password
4. Creates customer session
5. Redirects to customer dashboard

## ⚠️ **Note: Some Cross-Contamination Found**

There is one username that exists in both tables:
- **"riya"** exists as admin in User table AND as customer in Customer table

This is a data inconsistency that should be resolved, but the login system still works correctly because:

1. **Admin login** searches User table with `role='admin'` → finds admin "riya"
2. **Customer login** searches Customer table → finds customer "riya"

## 🎯 **Current Login Credentials**

### Admin Users (from User table)
```
Username: admin, Password: admin123
Username: Akanksha, Password: admin123
Username: akanksha, Password: admin123
Username: riya, Password: admin123
Username: aditi, Password: admin123
```

### Customer Users (from Customer table)
```
Username: margi, Password: (unknown)
Username: piyush, Password: (unknown)
Username: riya, Password: (unknown)
Username: testcustomer, Password: customer123
```

## ✅ **Database Separation Benefits**

1. **Security**: Admins and customers are stored separately
2. **Performance**: Faster queries for specific user types
3. **Scalability**: Can optimize each table independently
4. **Maintenance**: Easier to manage different user types
5. **Flexibility**: Different schemas for different user types

## 🔧 **Recommendations**

1. **Clean up legacy data**: Remove customer1 and customer2 from User table
2. **Resolve duplicate "riya"**: Decide which table should contain this user
3. **Standardize passwords**: Set known passwords for all test accounts
4. **Add constraints**: Ensure usernames are unique across both tables

## 🚀 **Current Status**

- ✅ **Separate tables exist**
- ✅ **Login verification works correctly**
- ✅ **Database separation is maintained**
- ✅ **Security features are active**
- ⚠️ **Some data cleanup needed**

The system is working correctly with the separate table structure! 