from flask import Flask
from .routes import init_routes
from .models import db, User
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # load configuration from Config class

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'danger'

    init_routes(app)

    return app