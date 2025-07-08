# Flavi Dairy Solutions: AI-Powered Demand & Inventory Forecasting

An intelligent web application that provides data-driven insights into demand forecasting for various dairy products (SKUs) and helps optimize inventory levels to maximize capacity utilization and reduce costs for Flavi Dairy Solutions.

## Project Overview

This system uses advanced time series forecasting techniques to predict future demand based on historical data, helping Flavi Dairy Solutions optimize their production and inventory management.

### Key Features

- Demand forecasting for individual SKUs
- Inventory level optimization
- Interactive dashboards for data visualization
- Capacity utilization tracking
- Stock-out and overstock alerts
- Production planning recommendations

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Database**: PostgreSQL
- **AI/ML**: Prophet, Pandas, NumPy, Scikit-learn
- **Deployment**: Docker, Heroku/Render

## Project Structure

```
Intel_project/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sku.py
│   │   ├── sales.py
│   │   └── inventory.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── api.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── base.html
│       └── index.html
├── ml/
│   ├── __init__.py
│   ├── data_processor.py
│   └── forecaster.py
├── tests/
│   └── __init__.py
├── config.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/flavi_db
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Development Timeline

- Week 1: Data Acquisition & AI Core
- Week 2: Database Integration & Basic UI
- Week 3: Advanced UI, Inventory Logic & Deployment

## Contributing

This project is part of the Intel AI internship program. For any questions or contributions, please contact the project maintainers.

## License

This project is proprietary and confidential. 