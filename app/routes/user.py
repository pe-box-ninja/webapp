from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("user", __name__)


@bp.route("/list")
@login_required
def list():
    return render_template("user/list.html", title="Users")


@bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", title="User profile")


@bp.route("/settings")
@login_required
def settings():
    return render_template("user/settings.html", title="Beállítások")
