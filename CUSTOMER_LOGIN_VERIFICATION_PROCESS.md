# Customer Login Verification Process

## Complete Flow: Click "Login as Customer" → Verify Data → Show Dashboard

### 1. User Action: Click "Login as Customer"

When a user clicks the "Login as Customer" button, this form is submitted:

```html
<form method="POST" action="{{ url_for('main.login') }}">
    <input type="hidden" name="login_type" value="customer">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login as Customer</button>
</form>
```

### 2. Backend Verification Process

#### Step 1: Form Data Processing
```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
elif login_type == 'customer':
    # Customer login verification from Customer table
    customer = Customer.query.filter_by(username=username).first()
    
    if customer and customer.check_password(password):
        # ✅ SUCCESS: Customer verified from Customer table
        login_user(customer)
        session['user_type'] = 'customer'
        session['user_id'] = customer.id
        session['username'] = customer.username
        
        print(f"✅ Customer login successful - Username: {username}, ID: {customer.id}")
        flash('Customer login successful! Welcome back.', 'success')
        return redirect(url_for('main.customer_dashboard'))
    else:
        # ❌ FAILED: Invalid credentials
        print(f"❌ Customer login failed - Username: {username}")
        flash('Invalid customer username or password. Please try again.', 'danger')
```

### 3. Database Verification Details

#### Customer Table Query
```python
# This query searches ONLY the Customer table
customer = Customer.query.filter_by(username=username).first()
```

**What happens:**
1. System searches `Customer` table for the username
2. If found, verifies password using `customer.check_password(password)`
3. If both username and password match → **SUCCESS**
4. If either username or password is wrong → **FAILED**

#### Password Verification
```python
def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

**Security features:**
- Password is hashed using Werkzeug
- Secure comparison prevents timing attacks
- No plain text passwords stored

### 4. Successful Login → Dashboard Redirection

#### Session Creation
```python
# Create secure session
login_user(customer)  # Flask-Login session
session['user_type'] = 'customer'  # Custom session data
session['user_id'] = customer.id
session['username'] = customer.username
```

#### Dashboard Redirection
```python
return redirect(url_for('main.customer_dashboard'))
```

### 5. Customer Dashboard Display

#### Dashboard Route Processing
```python
@bp.route('/customer_dashboard')
@login_required
def customer_dashboard():
    # Ensure this is a Customer instance
    if not isinstance(current_user, Customer):
        flash('Only customers can access this page.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Get customer information and statistics
    customer = Customer.query.filter_by(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email
    ).first()
    
    # Calculate order statistics
    orders = Order.query.filter_by(customer_id=customer.id).all()
    total_orders = len(orders)
    completed_orders = len([o for o in orders if o.status == 'completed'])
    pending_orders = len([o for o in orders if o.status == 'pending'])
    cancelled_orders = len([o for o in orders if o.status == 'cancelled'])
    
    # Get recent orders and available products
    recent_orders = orders[:5]
    skus = SKU.query.all()
    
    return render_template('customer_dashboard.html', 
                         customer=customer_info,
                         skus=skus,
                         recent_orders=recent_orders,
                         stats={
                             'total_orders': total_orders,
                             'completed_orders': completed_orders,
                             'pending_orders': pending_orders,
                             'cancelled_orders': cancelled_orders
                         })
```

### 6. Dashboard Content Display

The customer dashboard shows:

#### Customer Information Card
- Username, email, member since date
- Account status

#### Order Statistics Cards
- Total orders count
- Completed orders count
- Pending orders count
- Cancelled orders count

#### Quick Actions
- View Order History button
- Place New Order button
- Edit Profile button
- Logout button

#### Recent Orders Table
- Last 5 orders with status
- Link to full order history

#### Product Ordering Section
- Available products table
- Order and cancel functionality

### 7. Security Verification Points

#### 1. Database Separation
- ✅ Customers verified from `Customer` table only
- ✅ Admins verified from `User` table only
- ✅ No cross-contamination between user types

#### 2. Password Security
- ✅ Passwords hashed with Werkzeug
- ✅ Secure password verification
- ✅ No plain text storage

#### 3. Session Security
- ✅ Flask-Login session management
- ✅ Custom session data for user type
- ✅ Automatic session timeout

#### 4. Access Control
- ✅ Customer-specific routes protected
- ✅ Role-based access verification
- ✅ Automatic redirects for unauthorized access

### 8. Test the Complete Flow

#### Test Credentials
```
Username: testcustomer
Password: customer123
```

#### Test Steps
1. Go to: `http://127.0.0.1:5000/login`
2. Click "Customer Login" tab
3. Enter credentials above
4. Click "Login as Customer"
5. Verify redirection to customer dashboard
6. Check all dashboard sections are displayed

#### Expected Results
- ✅ Successful login message
- ✅ Redirect to customer dashboard
- ✅ Customer information displayed
- ✅ Order statistics shown
- ✅ Quick action buttons available
- ✅ Product ordering section visible

### 9. Error Handling

#### Invalid Credentials
```python
flash('Invalid customer username or password. Please try again.', 'danger')
```

#### Missing Fields
```python
flash('Username and password are required.', 'danger')
```

#### Database Errors
```python
except Exception as e:
    print(f"❌ Login error - Type: {login_type}, Username: {username}, Error: {str(e)}")
    flash('An error occurred during login. Please try again.', 'danger')
```

### 10. Logging and Monitoring

#### Success Logging
```python
print(f"✅ Customer login successful - Username: {username}, ID: {customer.id}")
```

#### Failure Logging
```python
print(f"❌ Customer login failed - Username: {username}")
```

#### Error Logging
```python
print(f"❌ Login error - Type: {login_type}, Username: {username}, Error: {str(e)}")
```

## Summary

The complete flow is:
1. **User clicks "Login as Customer"** → Form submission
2. **Backend receives data** → Input validation
3. **Database verification** → Search Customer table for username
4. **Password verification** → Secure hash comparison
5. **Session creation** → Flask-Login + custom session data
6. **Dashboard redirection** → Redirect to customer dashboard
7. **Dashboard display** → Show customer info, stats, and actions

This ensures secure, verified customer login with proper database separation and comprehensive dashboard functionality. 