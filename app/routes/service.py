from datetime import datetime

from flask import Blueprint, redirect, url_for, request
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
    login_date = datetime.utcnow()
    login_ip = request.remote_addr
    login_device = request.user_agent.string
    send_login_notification(
        user, login_date=login_date, login_ip=login_ip, login_device=login_device
    )
    return redirect(url_for("main.index"))


@bp.route("/welcome", methods=["GET"])
def service_welcome():
    user = User.query.filter_by(username="admin_martin").first()
    send_welcome_email(user)
    return redirect(url_for("main.index"))
