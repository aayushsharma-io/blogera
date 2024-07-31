from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
