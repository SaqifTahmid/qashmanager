from flask import Flask
from flask_login import LoginManager
from datamodels import db, bcrypt, account, ssdata
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tradingplatform.auth.registration import registeruser
from tradingplatform.auth.userlogin import loginuser

from tradingplatform.qashmanagerdata.topstocks import highest_traded
from purchaseorder import placeorder
from tradingplatform.env.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

#initializes Flask app with SQLAlchemy database
db.init_app(app)
#intializes bcrypt with app to allow password hashing
bcrypt.init_app(app)

app.register_blueprint(highest_traded, url_prefix='/info')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Inside the load_user function, this line queries the account table using the user ID passed as an argument. 
    # It retrieves the user object corresponding to the user ID from the database and returns it to Flask-Login.
    return account.query.get(int(user_id))

#register registration & login user blueprint with Flask App
registeruser(app)
loginuser(app)
app.register_blueprint(placeorder)

with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)