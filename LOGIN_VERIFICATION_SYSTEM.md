# Customer and Admin Login Verification System

## Overview

The Flavi Dairy Forecasting AI system implements a secure dual-table authentication system that separates customer and admin users into different database tables for enhanced security and data organization.

## Database Structure

### 1. Admin Users Table (`User`)
- **Table**: `user`
- **Purpose**: Stores admin users only
- **Key Fields**:
  - `id`: Primary key
  - `username`: Unique username
  - `email`: Unique email address
  - `password_hash`: Hashed password
  - `role`: Always set to 'admin'

### 2. Customer Users Table (`Customer`)
- **Table**: `customer`
- **Purpose**: Stores customer users only
- **Key Fields**:
  - `id`: Primary key
  - `username`: Unique username
  - `email`: Unique email address
  - `password_hash`: Hashed password
  - `role`: Always set to 'customer'
  - `created_at`: Account creation timestamp

## Login Verification Process

### Admin Login Verification
```python
# Admin login verification from User table
user = User.query.filter_by(username=username, role='admin').first()

if user and user.check_password(password):
    # Successful admin login
    login_user(user)
    session['user_type'] = 'admin'
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect(url_for('main.dashboard'))
else:
    # Failed admin login
    flash('Invalid admin username or password. Please try again.', 'danger')
```

### Customer Login Verification
```python
# Customer login verification from Customer table
customer = Customer.query.filter_by(username=username).first()

if customer and customer.check_password(password):
    # Successful customer login
    login_user(customer)
    session['user_type'] = 'customer'
    session['user_id'] = customer.id
    session['username'] = customer.username
    return redirect(url_for('main.customer_dashboard'))
else:
    # Failed customer login
    flash('Invalid customer username or password. Please try again.', 'danger')
```

## Security Features

### 1. Password Hashing
- All passwords are hashed using Werkzeug's `generate_password_hash()`
- Password verification uses `check_password_hash()`
- No plain text passwords are stored in the database

### 2. Input Validation
- Username and password are stripped of whitespace
- Empty credentials are rejected
- SQL injection protection through SQLAlchemy ORM

### 3. Session Management
- Uses Flask-Login for secure session management
- Session stores user type, ID, and username
- Automatic logout on session expiration

### 4. Access Control
- Customers can only access customer-specific pages
- Admins can only access admin-specific pages
- Role-based redirects after login

## Login Form Structure

The login page uses Bootstrap tabs to separate customer and admin login forms:

```html
<!-- Customer Login Tab -->
<div class="tab-pane fade show active" id="customer">
    <form method="POST" action="{{ url_for('main.login') }}">
        <input type="hidden" name="login_type" value="customer">
        <input type="text" name="username" required>
        <input type="password" name="password" required>
        <button type="submit">Login as Customer</button>
    </form>
</div>

<!-- Admin Login Tab -->
<div class="tab-pane fade" id="admin">
    <form method="POST" action="{{ url_for('main.login') }}">
        <input type="hidden" name="login_type" value="admin">
        <input type="text" name="username" required>
        <input type="password" name="password" required>
        <button type="submit">Login as Admin</button>
    </form>
</div>
```

## User Loader Function

The system uses a custom user loader that checks both tables:

```python
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    from app.models.customer import Customer

    # Try to find user in both tables
    user = User.query.get(int(user_id))
    if user:
        return user
    
    customer = Customer.query.get(int(user_id))
    if customer:
        return customer
    
    return None
```

## Error Handling and Logging

### Login Attempt Logging
```python
# Log login attempt (without sensitive data)
print(f"Login attempt - Type: {login_type}, Username: {username}")

# Successful login logging
print(f"✅ Admin login successful - Username: {username}, ID: {user.id}")
print(f"✅ Customer login successful - Username: {username}, ID: {customer.id}")

# Failed login logging
print(f"❌ Admin login failed - Username: {username}")
print(f"❌ Customer login failed - Username: {username}")
```

### Exception Handling
```python
try:
    # Login verification logic
    pass
except Exception as e:
    print(f"❌ Login error - Type: {login_type}, Username: {username}, Error: {str(e)}")
    flash('An error occurred during login. Please try again.', 'danger')
```

## Registration Process

### Customer Registration
1. Validates input (username, email, password)
2. Checks for existing users in both tables
3. Creates new customer in `Customer` table
4. Sets role to 'customer'

### Admin Registration
1. Validates input (username, email, password)
2. Checks for existing users in both tables
3. Creates new admin in `User` table
4. Sets role to 'admin'

## Testing the System

Run the test script to verify the login system:

```bash
python test_login_system.py
```

This will:
1. Check for admin users in User table
2. Check for customers in Customer table
3. Test password verification for both user types
4. Verify database table separation
5. Display sample login credentials

## Sample Login Credentials

Based on the test results:

### Admin Users
- Username: `admin`, Password: `admin123`
- Username: `Akanksha`, Password: `admin123`
- Username: `akanksha`, Password: `admin123`
- Username: `riya`, Password: `admin123`
- Username: `aditi`, Password: `admin123`

### Customer Users
- Username: `margi`, Password: `customer123`
- Username: `piyush`, Password: `customer123`
- Username: `riya`, Password: `customer123`

## Security Best Practices

1. **Password Requirements**: Minimum 6 characters
2. **Email Validation**: Basic regex validation
3. **Username Uniqueness**: Enforced across both tables
4. **Session Security**: Automatic timeout and secure session handling
5. **Error Messages**: Generic error messages to prevent information leakage
6. **Input Sanitization**: All inputs are stripped and validated

## Troubleshooting

### Common Issues

1. **Login Fails**: Check if user exists in correct table
2. **Password Issues**: Verify password hashing is working
3. **Session Problems**: Check Flask-Login configuration
4. **Database Errors**: Verify database connection and table structure

### Debug Commands

```python
# Check admin users
admin_users = User.query.filter_by(role='admin').all()

# Check customers
customers = Customer.query.all()

# Test password verification
user.check_password('password')
```

## Future Enhancements

1. **Two-Factor Authentication**: Add SMS or email verification
2. **Password Reset**: Implement secure password reset functionality
3. **Account Lockout**: Add brute force protection
4. **Audit Logging**: Track all login attempts and user actions
5. **Role-Based Permissions**: Implement granular permission system 