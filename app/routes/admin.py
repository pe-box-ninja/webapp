from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User
from app.decorators import admin_required

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template("admin/index.html", title="Admin Dashboard", users=users)


@bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template("admin/users.html", title="User Management", users=users)
