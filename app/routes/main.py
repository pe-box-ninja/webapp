from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    abort,
    send_from_directory,
)
from flask_login import login_required, current_user
from app.models import User
from app.decorators import admin_required
from app.algo_viz import simulate_delivery
import os

bp = Blueprint("main", __name__)


@bp.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@bp.route("/")
@bp.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html", title="Főoldal")


@bp.route("/dashboard")
@login_required
def dashboard():
    return redirect(url_for("package.list"))


@bp.route("/admin")
@login_required
@admin_required
def admin():
    if not current_user.is_admin():
        abort(403)  # Forbidden
    users = User.query.all()
    return render_template("admin/index.html", title="Admin Irányítópult", users=users)


@bp.route("/admin/design-system")
def secret_design_system():
    if not current_user.is_admin():
        abort(403)
    return render_template("admin/design-system.html", title="Design System")


@bp.route("/algo")
def algo_viz():
    simulation_data = simulate_delivery()
    return render_template(
        "algo/algo.html",
        title="Algoritmus Vizualizáció",
        simulation_data=simulation_data,
    )
