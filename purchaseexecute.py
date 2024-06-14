import requests
from datamodels import db, buy
from apscheduler.schedulers.background import BackgroundScheduler
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.config import IEX_API_TOKEN

def check_and_execute_orders():
    pending_orders = buy.query.filter_by(status='pending').all()
    for buy in pending_orders:
        cprice = fetch_current_price(buy.stock_symbol)
        
        if buy.otype == 'market':
            execute_order(buy, cprice)
        elif buy.otype == 'limit' and cprice <= buy.target_price:
            execute_order(buy, cprice)
        elif buy.otype == 'stop' and cprice >= buy.stop_price:
            execute_order(buy, cprice)
        elif buy.otype == 'stop_limit' and cprice >= buy.stop_price:
            if cprice <= buy.target_price:
                execute_order(buy, cprice)

def fetch_current_price(stock_symbol):
    # Use IEX API to fetch current price
    url = f"https://cloud.iexapis.com/stable/stock/{stock_symbol}/quote"
    params = {'token': IEX_API_TOKEN}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['latestPrice']
    return None

def execute_order(buy, price):
    buy.status = 'executed'
    buy.pprice = price
    db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_and_execute_orders, trigger="interval", seconds=60)
scheduler.start()
