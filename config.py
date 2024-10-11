import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Determine the host and port dynamically
    BASE_URL = os.environ.get("BASE_URL") or "http://127.0.0.1:5000"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration for MailHog
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 1025)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER") or "noreply@boxninja.com"
    )
