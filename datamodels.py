from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db=SQLAlchemy()
bcrypt=Bcrypt()

#model: method for storing account
class account(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(80), unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    #generate hashesd password using bcrypt
    def setpass(self, password):
        self.sethash=bcrypt.generate_password_hash(password).decode('utf-8')
    
    #verify provided password against stored hashed password
    def checpass(self, password):
        return bcrypt.check_password_hash(self.sethash, password)
    
    def __repr__(self):
        return f"accountID:('{self.username}', '{self.email}')"

#model: method for starting session
class ssdata(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    session_id = db.Column(db.String(32), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Session {self.session_id}>"
    
#model: method to store buy and sell stock
class buy(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    otype = db.Column(db.String(20), nullable=True) 
    quantity = db.Column(db.Integer, nullable=False)
    target_price = db.Column(db.Float)  
    stop_price = db.Column(db.Float) 
    status = db.Column(db.String(20), default='pending')
    purchase_price= db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.id} - {self.stock_symbol} - {self.otypetype}>"

#model: method to store  
class portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    average_purchase_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Portfolio('{self.user_id}', '{self.stock_symbol}', '{self.quantity}', '{self.purchase_price}')"