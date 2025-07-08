# Customer Login Flow and Redirection Guide

## Overview

This guide explains the complete customer login flow, from clicking "Customer Login" to being redirected to the customer dashboard after successful authentication.

## Complete Login Flow

### 1. Initial Login Page Access
- **URL**: `http://127.0.0.1:5000/login`
- **Page**: Login page with two tabs (Customer Login and Admin Login)

### 2. Customer Login Tab Selection
- User clicks on the "Customer Login" tab
- The tab becomes active and shows the customer login form
- The form includes:
  - Username field
  - Password field
  - "Login as Customer" button
  - Registration link
  - Forgot password link

### 3. Form Submission Process
When user clicks "Login as Customer":

```html
<form method="POST" action="{{ url_for('main.login') }}">
    <input type="hidden" name="login_type" value="customer">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login as Customer</button>
</form>
```

### 4. Backend Verification Process

#### Step 1: Input Validation
```python
username = request.form.get('username', '').strip()
password = request.form.get('password', '')
login_type = request.form.get('login_type', 'customer')

# Input validation
if not username or not password:
    flash('Username and password are required.', 'danger')
    return render_template('login.html')
```

#### Step 2: Customer Database Verification
```python
# Customer login verification from Customer table
customer = Customer.query.filter_by(username=username).first()

if customer and customer.check_password(password):
    # Successful customer login
    login_user(customer)
    session['user_type'] = 'customer'
    session['user_id'] = customer.id
    session['username'] = customer.username
    
    print(f"✅ Customer login successful - Username: {username}, ID: {customer.id}")
    flash('Customer login successful! Welcome back.', 'success')
    return redirect(url_for('main.customer_dashboard'))
else:
    # Failed customer login
    print(f"❌ Customer login failed - Username: {username}")
    flash('Invalid customer username or password. Please try again.', 'danger')
```

### 5. Successful Login Redirection

#### Redirect to Customer Dashboard
After successful verification, the system:
1. Creates a user session using Flask-Login
2. Stores user information in session
3. Redirects to `/customer_dashboard`

#### Customer Dashboard Features
The enhanced customer dashboard now includes:

1. **Customer Information Card**
   - Username, email, member since date
   - Account status

2. **Order Statistics Cards**
   - Total orders
   - Completed orders
   - Pending orders
   - Cancelled orders

3. **Quick Actions**
   - View Order History
   - Place New Order
   - Edit Profile
   - Logout

4. **Recent Orders Table**
   - Shows last 5 orders
   - Order status with color-coded badges
   - Link to full order history

5. **Product Ordering Section**
   - Available products table
   - Order and cancel functionality
   - Responsive design

### 6. Navigation Options

From the customer dashboard, users can:

- **View Order History**: Navigate to detailed order history page
- **Place New Orders**: Use the product ordering section
- **Edit Profile**: Access customer profile settings
- **Logout**: Securely log out of the system

## Security Features

### 1. Database Separation
- Customers are stored in `Customer` table
- Admins are stored in `User` table
- No cross-contamination between user types

### 2. Password Security
- All passwords are hashed using Werkzeug
- Secure password verification
- No plain text storage

### 3. Session Management
- Flask-Login for secure session handling
- Session stores user type, ID, and username
- Automatic session timeout

### 4. Access Control
- Customer-specific routes protected
- Role-based access verification
- Automatic redirects for unauthorized access

## Error Handling

### 1. Invalid Credentials
- Generic error message: "Invalid customer username or password"
- No information leakage about which field is wrong
- Logging of failed attempts

### 2. Missing Fields
- Validation for required username and password
- Clear error messages for missing data

### 3. Database Errors
- Exception handling for database issues
- Graceful error messages
- Logging of technical errors

## Testing the Flow

### Manual Testing Steps
1. Navigate to `http://127.0.0.1:5000/login`
2. Click "Customer Login" tab
3. Enter valid customer credentials
4. Click "Login as Customer"
5. Verify redirection to customer dashboard
6. Test navigation between dashboard and order history

### Sample Customer Credentials
Based on the database:
- Username: testcustomer, Password: customer123

## Expected User Experience

### 1. Login Process
- User sees clear login form
- Form validation provides immediate feedback
- Success message confirms login
- Smooth redirection to dashboard

### 2. Dashboard Experience
- Welcome message with customer name
- Clear overview of account status
- Easy access to all customer functions
- Responsive design for all devices

### 3. Navigation
- Intuitive navigation between sections
- Clear action buttons
- Consistent user interface
- Smooth transitions

## Technical Implementation

### 1. Route Structure
```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Handle both customer and admin login

@bp.route('/customer_dashboard')
@login_required
def customer_dashboard():
    # Show customer dashboard with stats and actions

@bp.route('/customer_order_history')
@login_required
def customer_order_history():
    # Show detailed order history
```

### 2. Template Structure
- `login.html`: Dual-tab login form
- `customer_dashboard.html`: Enhanced dashboard with statistics
- `customer_order_history.html`: Detailed order history
- `customer_base.html`: Customer-specific navigation

### 3. Database Models
- `Customer`: Customer-specific user model
- `Order`: Order tracking model
- `SKU`: Product catalog model

## Troubleshooting

### Common Issues
1. **Login Fails**: Check if customer exists in Customer table
2. **Password Issues**: Verify password hashing is working
3. **Redirect Problems**: Check route definitions and permissions
4. **Session Issues**: Verify Flask-Login configuration

### Debug Commands
```python
# Check customer in database
customer = Customer.query.filter_by(username='margi').first()

# Test password verification
customer.check_password('password')

# Check session data
session.get('user_type')
session.get('user_id')
```

## Future Enhancements

1. **Two-Factor Authentication**: Add SMS or email verification
2. **Password Reset**: Implement secure password reset
3. **Account Lockout**: Add brute force protection
4. **Audit Logging**: Track all customer actions
5. **Email Notifications**: Order status updates
6. **Mobile App**: Native mobile application 