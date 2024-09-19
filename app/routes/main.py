from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models import User
from app.decorators import admin_required

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html", title="Főoldal")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Irányítópult")


@bp.route("/admin")
@login_required
@admin_required
def admin():
    if not current_user.is_admin():
        abort(403)  # Forbidden
    users = User.query.all()
    return render_template("admin/index.html", title="Admin Irányítópult", users=users)


@bp.route("/admin/design-system")
@login_required
@admin_required
def secret_design_system():
    if not current_user.is_admin():
        abort(403)
    return render_template("admin/design-system.html", title="Design System")
