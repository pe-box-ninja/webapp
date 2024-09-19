from flask import Blueprint, render_template
from flask_login import login_required
from app import db

bp = Blueprint("admin", __name__)


@bp.route("/index")
@login_required
def index():
    return render_template("admin/index.html", title="Admin Dashboard")
