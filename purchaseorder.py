from flask import Blueprint, request, jsonify
from datamodels import db, buy
from flask_login import login_required, current_user

placeorder= Blueprint('buy', __name__)

@placeorder.route('/<username>/purchase-buy', methods=['POST'])
@login_required
def purchase():
    data=request.json
    stock_symbol = data.get('stock_symbol')
    otype = data.get('otype')
    quantity = data.get('quantity')
    target_price = data.get('target_price')
    stop_price = data.get('stop_price')

    # Validate the input data
    if not stock_symbol or not otype or not quantity:
        return jsonify({'error': 'stock symbol, buy type, and quantity are required fields'}), 400
    
    # Handle market buy specifically
    if otype == 'market':
        target_price = None
        stop_price = None
    
    # Create a new buy instance with the extracted data
    new_order =buy(
        user_id=current_user.id,
        stock_symbol=stock_symbol,
        otype=otype,
        quantity=quantity,
        target_price=target_price,
        stop_price=stop_price,
        status= 'pending'
    )
    
    # Add and commit the new buy to the database
    db.session.add(new_order)
    db.session.commit()
