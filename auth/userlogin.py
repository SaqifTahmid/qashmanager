from flask import Blueprint, redirect, request, jsonify, session, url_for
from datamodels import db, account, ssdata, portfolio
from flask_login import login_user, logout_user, login_required
import uuid

login_bp = Blueprint('login', __name__)

def ssidgen():
    while True:
        session_id = uuid.uuid4().hex
        existing_session = ssdata.query.filter_by(session_id=session_id).first()
        if not existing_session:
            return session_id

@login_bp.route('/login', methods=['POST'])
def userlogin():
    #login user using data received from frontend
    data = request.json
    loginfo = data.get('Login')
    password = data.get('password')
    
    # Check if user exists in database
    user = account.query.filter((account.username == loginfo) | (account.email == loginfo)).first()
    
    if user and user.checkpass(password):
        # Login successful
        login_user(user) 
        
        # Generate a unique session ID
        session_id = ssidgen()
        
        # Create a new session entry in the database
        new_session = ssdata(user_id=user.id, session_id=session_id)
        db.session.add(new_session)
        db.session.commit()
        
        # Store session ID in the Flask session
        session['session_id'] = session_id
        
        return redirect(url_for('profile', username=user.username)), 200
    else:
        return jsonify({'Error': 'Invalid Credentials'}), 401


@login_bp.route('/<username>', methods=['GET'])
@login_required
def profile(username):
    user= account.query.filter_by(username=username).first()
    if user.username != username:
        return jsonify({'error': 'Unauthorized access to user portfolio'}), 403
    
    user_portfolio = portfolio.query.filter_by(user_id=user.id).all()
    portfolio_data = [{'stock_symbol': client.stock_symbol, 'quantity': client.quantity,\
        'average_purchase_price': client.average_purchase_price} for client in user_portfolio]
    return portfolio_data


@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # Get the current session ID
    session_id = session.get('session_id')
    
    if session_id:
        # Remove the session entry from the database
        ssdata.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        
        # Clear the session cookie
        session.pop('session_id', None)
    
    # Log the user out
    logout_user()
    
    return jsonify({'Message': 'Logout Successful!'}), 200

def loginuser(app):
    app.register_blueprint(login_bp, url_prefix='/auth')
