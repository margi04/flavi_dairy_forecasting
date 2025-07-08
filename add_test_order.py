from app import create_app, db
from app.models.order import Order
from app.models.sku import SKU
from app.models.user import User
from datetime import datetime

app = create_app()

with app.app_context():
    # Prompt for username or user ID
    user_input = input('Enter username or user ID to add a test order for: ')
    user = None
    if user_input.isdigit():
        user = User.query.filter_by(id=int(user_input)).first()
    else:
        user = User.query.filter_by(username=user_input).first()
    if not user:
        print('User not found!')
        exit(1)
    # Pick a SKU
    sku = SKU.query.first()
    if not sku:
        print('No SKUs found!')
        exit(1)
    # Create a test order
    order = Order(
        customer_id=user.id,
        sku_id=sku.sku_id,
        quantity=2,
        status='pending',
        created_at=datetime.now()
    )
    db.session.add(order)
    db.session.commit()
    print(f'Test order added for user {user.username} (ID: {user.id}) with SKU {sku.sku_id}.') 