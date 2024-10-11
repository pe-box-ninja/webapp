from datetime import datetime

from flask import Blueprint, redirect, url_for
from app.models import User
from app.email import (
    send_welcome_email,
    send_login_notification,
    send_delivery_notification,
)


bp = Blueprint("service", __name__)


@bp.route("/delivery", methods=["GET"])
def service_delivery():
    user = User.query.filter_by(username="admin_martin").first()
    send_delivery_notification(user, tracking_number="bn1")
    return redirect(url_for("main.index"))


@bp.route("/login", methods=["GET"])
def service_login():
    user = User.query.filter_by(username="admin_martin").first()
    random_ip = "127.0.0.1"
    browser = "Chrome"
    send_login_notification(
        user, login_date=datetime.now(), login_ip=random_ip, login_device=browser
    )
    return redirect(url_for("main.index"))


@bp.route("/welcome", methods=["GET"])
def service_welcome():
    user = User.query.filter_by(username="admin_martin").first()
    send_welcome_email(user)
    return redirect(url_for("main.index"))
