from flask import Flask
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16MB max file size

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User  # Ensure User model is imported

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from app.routes import bp as main_bp
app.register_blueprint(main_bp)
