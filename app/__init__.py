from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import main, package, courier, warehouse, user, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(package.bp)
    app.register_blueprint(courier.bp)
    app.register_blueprint(warehouse.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)

    return app

from app import models