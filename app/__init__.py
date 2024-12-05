from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
mail = Mail()

# Swagger configuration
SWAGGER_URL = "/api/docs"
API_URL = "/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "BoxNinja API", "defaultModelsExpandDepth": -1},
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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
        swagger,
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
    app.register_blueprint(swagger.bp)

    return app


from app import models
