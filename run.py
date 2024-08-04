import os
from flask import Flask
from flask_login import LoginManager
from app.models import User  # Assuming User is defined in app/models.py

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16MB max file size

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.admin_login'  # Redirect unauthorized users to login page

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)  # Assuming User.get method fetches user by ID

from app import routes

app.register_blueprint(routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
