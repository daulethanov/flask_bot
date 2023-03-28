from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from flask_bot.admin.admin import admin
from flask_jwt_extended import JWTManager
from .views.auth import auth, login_manager
from .model.user import user_datastore
from .config.base import Config
from .model import db
from .views.ticket import ticket


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)
    security = Security(app, user_datastore)
    jwt = JWTManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_users'
    admin.init_app(app)

    app.register_blueprint(ticket)
    app.register_blueprint(auth)

    return app

