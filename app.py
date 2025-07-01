from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, DemandData, ForecastHistory
from forecasting import prepare_series, train_arima, forecast_demand
import pandas as pd
import json
import os
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flavi_dairy.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can login now.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('No file selected.', 'danger')
            return redirect(url_for('upload'))

        # Read without parse_dates first
        df = pd.read_csv(file)

        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        # Check required columns
        required_cols = {'date', 'sku', 'quantity'}
        if not required_cols.issubset(set(df.columns)):
            flash(f'Missing required columns: {required_cols - set(df.columns)}', 'danger')
            return redirect(url_for('upload'))

        # Parse date safely
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Drop rows with invalid dates or missing values
        df = df.dropna(subset=['date', 'sku', 'quantity'])

        # Insert into DB
        for _, row in df.iterrows():
            try:
                entry = DemandData(
                    date=row['date'],
                    sku=row['sku'],
                    quantity=int(row['quantity'])
                )
                db.session.add(entry)
            except Exception as e:
                flash(f"Error adding row: {e}", 'danger')
                db.session.rollback()
                return redirect(url_for('upload'))

        db.session.commit()
        flash('Data uploaded successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('upload.html')


@app.route('/manual_add', methods=['GET', 'POST'])
@login_required
def manual_add():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            sku = request.form['sku']
            quantity_str = request.form['quantity']

            if not date_str or not sku or not quantity_str:
                flash('All fields are required.', 'danger')
                return redirect(url_for('manual_add'))

            date = datetime.strptime(date_str, '%Y-%m-%d')
            quantity = int(quantity_str)

            entry = DemandData(date=date, sku=sku, quantity=quantity)
            db.session.add(entry)
            db.session.commit()
            flash('Record added successfully.', 'success')
            return redirect(url_for('dashboard'))

        except ValueError as e:
            flash(f'Invalid input: {e}', 'danger')
            return redirect(url_for('manual_add'))

    return render_template('manual_add.html')


@app.route('/forecast', methods=['GET', 'POST'])
@login_required
def forecast_view():
    skus = [row[0] for row in db.session.query(DemandData.sku).distinct().all()]

    if request.method == 'POST':
        sku = request.form['sku']
        days = int(request.form['days'])

        query = db.session.query(DemandData).filter_by(sku=sku).order_by(DemandData.date)
        rows = query.all()

        if not rows:
            flash("No data found for selected SKU.")
            return redirect(url_for('forecast_view'))

        df = pd.DataFrame([{
            'date': r.date,
            'sku': r.sku,
            'quantity': r.quantity
        } for r in rows])

        df = df.sort_values('date')
        df.set_index('date', inplace=True)

        # Forecasting
        model = ARIMA(df['quantity'], order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=days)
        forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days)

        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'predicted_quantity': forecast
        })

        # Plotly chart
        trace_past = go.Scatter(
            x=df.index,
            y=df['quantity'],
            mode='lines+markers',
            name='Historical Data'
        )
        trace_forecast = go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['predicted_quantity'],
            mode='lines+markers',
            name='Forecast'
        )
        layout = go.Layout(
            title=f'Demand Forecast for {sku}',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Quantity'},
            template='plotly_white'
        )
        fig = go.Figure(data=[trace_past, trace_forecast], layout=layout)
        graph_html = pyo.plot(fig, output_type='div')

        return render_template(
            'forecast.html',
            skus=skus,
            forecast_table=forecast_df.to_html(index=False),
            graph_html=graph_html
        )

    return render_template('forecast.html', skus=skus)



@app.route('/history')
@login_required
def history():
    records = ForecastHistory.query.order_by(ForecastHistory.forecast_date.desc()).all()
    all_forecasts = []
    for rec in records:
        forecasts = pd.read_json(rec.forecast_values)
        all_forecasts.append({
            'sku': rec.sku,
            'date': rec.forecast_date.strftime('%Y-%m-%d'),
            'data': forecasts.to_dict(orient='records')
        })
    return render_template('history.html', forecasts=all_forecasts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
