#Flask
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
#Password hashing
from werkzeug.security import generate_password_hash, check_password_hash
#Datetime for token expiration
import datetime
#ENV
from dotenv import load_dotenv
import os
# MongoDB
from modules import auth
# Regex For Email Validation
import re

load_dotenv() #Load .env file

jwt_key = os.getenv('JWT_SECRET_KEY')
connection_string = os.getenv('DB_CONNECTION_STRING')

db = auth.database(connection_string)

# Flask app initialization
app = Flask(__name__)

# JWT initialization
app.config['JWT_SECRET_KEY'] = jwt_key
jwt = JWTManager(app)

#
# API
#

# Register endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({'msg': 'Fill All The Fields', 'code' : 400}), 200
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'msg': 'Invalid Email', 'code' : 400}), 200

    if db.query_email(email): # Check if email is already registered
        return jsonify({'msg': 'Email Already Used', 'code' : 400}), 200

    if db.query_username(username): # Check if username is already registered
        return jsonify({'msg': 'Username Already Used', 'code' : 400}), 200

    hashed_password = generate_password_hash(password)
    user_id = db.insert_user(email, hashed_password, username)
    
    return jsonify({
        'code' : 200,
        'msg': 'Registration Successful',
        'data': {'user_id' : str(user_id)} 
    }), 200

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password: # Check if email and password are provided
        return jsonify({'msg': 'Fill All The Fields', 'code' : 400}), 200

    user = db.query_email(email)
    
    if not user: # If the user is not found
        return jsonify({'msg': 'Credentials Are Not Valid', 'code' : 401}), 200
    
    hash_check = check_password_hash(user['password'], password)
    
    if not hash_check: # If the password is not correct
        return jsonify({'msg': 'Credentials Are Not Valid', 'code' : 401}), 200
    
    # If the user is found and the password is correct, create a JWT token
    access_token = create_access_token(identity=str(user['_id']), expires_delta=datetime.timedelta(hours=1))
    response = jsonify({
        'code' : 200,
        'data' :{
            'access_token': access_token,
            'username' : user["username"],
            'user_id' : str(user['_id']) 
        }
    })

    return response

# Dashboard endpoint (protected test endpoint)
# This endpoint is protected by JWT, so it requires a valid token to be accessed
@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity() # Get the user_id from the token
    if current_user_id: # If the token is valid
        user = db.query_user(current_user_id)
        if not user:
            return jsonify({'msg': 'User Not Found', 'code' : 404}), 200
        return jsonify({
            'code' : 200,
            'data': {'username' : str(user["username"]) , 'email' : str(user["email"])}
        }), 200
    else: # If the token is not valid
        return jsonify({'msg': 'Token Not Valid', 'code' : 401}), 200

#
# Web pages
#

@app.route('/login' , methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/register' , methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/dashboard' , methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
