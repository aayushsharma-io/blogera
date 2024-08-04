import json

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
                for user in users:
                    if user['id'] == user_id:
                        return User(user['id'], user['username'], user['password'])
        except FileNotFoundError:
            return None
        return None

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
