from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.routes import (
        main,
        package,
        courier,
        warehouse,
        user,
        auth,
        parcel_locker,
        admin,
        service,
        cdn,
    )

    app.register_blueprint(main.bp, url_prefix="/")
    app.register_blueprint(auth.bp, url_prefix="/")
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(parcel_locker.bp, url_prefix="/parcel_locker")
    app.register_blueprint(package.bp, url_prefix="/package")
    app.register_blueprint(courier.bp, url_prefix="/courier")
    app.register_blueprint(warehouse.bp, url_prefix="/warehouse")
    app.register_blueprint(user.bp, url_prefix="/user")
    app.register_blueprint(service.bp, url_prefix="/service")
    app.register_blueprint(cdn.bp, url_prefix="/cdn")

    return app


from app import models
