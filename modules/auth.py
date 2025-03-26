from pymongo import MongoClient
from bson.objectid import ObjectId

class database:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['auth_db']
        self.users_collection = self.db['users']
    
    def query_email(self, email):
        users = self.users_collection.find_one({'email': email})
        return users
    
    def insert_user(self, email, password, username):
        user_id = self.users_collection.insert_one({'email': email, 'password': password, 'username' : username})
        return user_id.inserted_id

    def query_user(self, user_id):
        user = self.users_collection.find_one({'_id': ObjectId(user_id)})
        return user
    
    def query_username(self, username):
        user = self.users_collection.find_one({'username': username})
        return user