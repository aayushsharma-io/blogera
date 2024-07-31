from flask_login import UserMixin
import json
import os

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        if not os.path.exists('app/data/users.json'):
            return None

        with open('app/data/users.json', 'r') as f:
            users = json.load(f)
            user = next((u for u in users if u['id'] == int(user_id)), None)
            if user:
                return User(user['id'], user['username'])
            return None
