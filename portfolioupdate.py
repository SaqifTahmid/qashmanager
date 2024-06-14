from datamodels import db,buy,portfolio

def status_check():
    executed=buy.query.filter_by(status='executed').all()
    
    for buy in executed:
        #add executed orders to portfolio
        addport(buy.user_id, buy.stock_symbol,\
            buy.quantity, buy.pprice, buy.status)
        #delete order from db
        db.session.delete(buy)
        
    db.session.commit()

def addport(user_id, stock_symbol,  quantity, price):
    xstock = portfolio.query.filter_by(user_id=user_id, stock_symbol=stock_symbol).first()

    if xstock:
        # Update the existing entry
        xstock.quantity += quantity
        xstock.average_purchase_price = ((xstock.quantity *\
            xstock.average_purchase_price) + (quantity * price)) / \
                (xstock.quantity + quantity)
        db.session.commit()
    else:
        # Create a new entry
        insert= portfolio(user_id=user_id, stock_symbol=stock_symbol,\
            quantity=quantity, average_purchase_price=price)
        db.session.add(insert)
        db.session.commit()