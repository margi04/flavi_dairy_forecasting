from app import create_app, db
from app.models.sales import Sales
from datetime import date, timedelta

app = create_app()
with app.app_context():
    today = date.today()
    for i in range(30):
        sales = Sales(
            sku_id='MILK-1L',
            date=today - timedelta(days=i),
            quantity_sold=100 + i,  # Example: increasing sales
            revenue=50 * (100 + i)  # Example: revenue
        )
        db.session.add(sales)
    db.session.commit()
    print("Sample sales data for MILK-1L added.") 