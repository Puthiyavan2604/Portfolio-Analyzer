from flask import Flask, render_template, request, redirect, url_for, send_file, flash, Response
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_portfolio_csv(path_or_buffer):
    df = pd.read_csv(path_or_buffer)
    col_map = {c: c.strip() for c in df.columns}
    df.rename(columns=col_map, inplace=True)
    cols_lower = {c.lower(): c for c in df.columns}
    
    stock_col = None
    for candidate in ['stock', 'stock name', 'symbol', 'ticker']:
        if candidate in cols_lower:
            stock_col = cols_lower[candidate]
            break
            
    if stock_col is None:
        raise ValueError('CSV must contain a column for stock name (e.g. Stock, Stock Name, Symbol, Ticker)')
        
    date_col = None
    for candidate in ['date', 'day', 'timestamp']:
        if candidate in cols_lower:
            date_col = cols_lower[candidate]
            break
            
    if date_col is None:
        raise ValueError('CSV must contain a column for date (e.g. Date)')
        
    price_col = None
    for candidate in ['price', 'close', 'close price', 'value']:
        if candidate in cols_lower:
            price_col = cols_lower[candidate]
            break
            
    if price_col is None:
        raise ValueError('CSV must contain a column for price (e.g. Price, Close)')
        
    df = df[[stock_col, date_col, price_col]].copy()
    df.columns = ['Stock', 'Date', 'Price']
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Stock', 'Date', 'Price']).reset_index(drop=True)
    return df

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        save_path = os.path.join(UPLOAD_FOLDER, 'uploaded_portfolio.csv')
        file.save(save_path)
        flash('File uploaded successfully')
        return redirect(url_for('summary'))
    else:
        flash('Please upload a CSV file')
        return redirect(url_for('index'))

@app.route('/summary')
def summary():
    uploaded = os.path.join(UPLOAD_FOLDER, 'uploaded_portfolio.csv')
    sample = os.path.join(os.path.dirname(__file__), 'sample_portfolio.csv')
    source = uploaded if os.path.exists(uploaded) else sample
    
    try:
        df = read_portfolio_csv(source)
    except Exception as e:
        return render_template('error.html', message=str(e))
        
    total_records = len(df)
    unique_stocks = df['Stock'].nunique()
    overall_avg_price = round(df['Price'].mean(), 2) if total_records > 0 else 0.0
    
    stats = []
    grouped = df.sort_values(['Stock', 'Date']).groupby('Stock', sort=True)
    
    for stock, g in grouped:
        records = len(g)
        min_price = round(g['Price'].min(), 2)
        max_price = round(g['Price'].max(), 2)
        avg_price = round(g['Price'].mean(), 2)
        
        first_price = float(g.sort_values('Date')['Price'].iloc[0])
        last_price = float(g.sort_values('Date')['Price'].iloc[-1])
        price_change = round(last_price - first_price, 2)
        volatility = round(g['Price'].std(ddof=0) if records > 1 else 0.0, 2)
        
        stats.append({
            'Stock': stock,
            'Records': records,
            'Min': min_price,
            'Max': max_price,
            'Avg': avg_price,
            'Change': price_change,
            'Volatility': volatility
        })
        
    return render_template('summary.html', total_records=total_records, unique_stocks=unique_stocks, overall_avg_price=overall_avg_price, stats=stats)

@app.route('/plots', methods=['GET', 'POST'])
def plots():
    uploaded = os.path.join(UPLOAD_FOLDER, 'uploaded_portfolio.csv')
    sample = os.path.join(os.path.dirname(__file__), 'sample_portfolio.csv')
    source = uploaded if os.path.exists(uploaded) else sample
    
    try:
        df = read_portfolio_csv(source)
    except Exception as e:
        return render_template('error.html', message=str(e))
        
    stocks = sorted(df['Stock'].unique())
    selected = request.values.get('stock') or (stocks[0] if stocks else None)
    
    if selected:
        g = df[df['Stock'] == selected].sort_values('Date')
    else:
        g = pd.DataFrame(columns=df.columns)
        
    if request.args.get('img') == '1' and selected:
        fig = Figure(figsize=(8, 4))
        ax = fig.subplots()
        ax.plot(g['Date'], g['Price'])
        ax.set_title(f'{selected} Price Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        fig.autofmt_xdate()
        
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        output.seek(0)
        return Response(output.getvalue(), mimetype='image/png')
        
    return render_template('plots.html', stocks=stocks, selected=selected, table=g.to_dict(orient='records'))

@app.route('/download/sample')
def download_sample():
    path = os.path.join(os.path.dirname(__file__), 'sample_portfolio.csv')
    return send_file(path, as_attachment=True, download_name='sample_portfolio.csv')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
