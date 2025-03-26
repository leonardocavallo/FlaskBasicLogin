#Flask
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#Hashing password
from werkzeug.security import generate_password_hash, check_password_hash
#Data per durata token
import datetime
#ENV
from dotenv import load_dotenv
import os
# MongoDB
from modules import auth

load_dotenv() #Carichiamo Env

jwt_key = os.getenv('JWT_SECRET_KEY')
connection_string = os.getenv('DB_CONNECTION_STRING')

db = auth.database(connection_string)

# Inizializzazione Flask
app = Flask(__name__)

# Configurazione JWT
app.config['JWT_SECRET_KEY'] = jwt_key
jwt = JWTManager(app)



@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    if db.query_email(email):
        return jsonify({'msg': 'Email già registrata'}), 400

    hashed_password = generate_password_hash(password)
    user_id = db.insert_user(email, hashed_password, username)
    
    return jsonify({'msg': 'Registrazione completata', 'user_id': str(user_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = db.query_email(email)
    hash_check = check_password_hash(user['password'], password)
    if not user or not hash_check: # Se fallisce il controllo della password o l'utente non esiste
        return jsonify({'msg': 'Credenziali non valide'}), 401
    
    # Se le credenziali sono corrette, generiamo il token
    access_token = create_access_token(identity=str(user['_id']), expires_delta=datetime.timedelta(hours=1))
    return jsonify({'access_token': access_token, 'username' : user["username"], 'user_id' : str(user['_id'])})

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = db.query_user(current_user_id)
    return jsonify({'msg': f'Accesso autorizzato per user {str(user["username"])}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
