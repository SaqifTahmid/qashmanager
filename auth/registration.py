from flask import Blueprint, request, jsonify
from datamodels import db, account
import uuid

registration = Blueprint('register', __name__)

@registration.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    #check for input validity
    if not username or not email or not password:
        return jsonify({'error_Null': 'Please provide username, email, and password'}), 400
    
    #check for existing
    user_query = account.query.filter((account.username == username) | (account.email == email)).first()
    if user_query:
        return jsonify({'error_Input_Exists': 'Username or email already exists'}), 400
    
    #create new user
    new_account = account(username=username, email=email)
    new_account.setpass(password)
    
    db.session.add(new_account)
    db.session.commit()    
    
    return jsonify({"message": "Account registered successfully", "username": new_account.username}), 201

def registeruser(app):
    app.register_blueprint(registration, url_prefix='/auth')
