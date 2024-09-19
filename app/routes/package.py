from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.models import Package
from app.decorators import warehouse_required

bp = Blueprint("package", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    packages = Package.query.all()
    return render_template("package/list.html", title="Packages", packages=packages)


@bp.route("/send")
@login_required
def send():
    return render_template("package/send.html", title="Send Package")


@bp.route("/track", methods=["GET", "POST"])
def track():
    if request.method == "POST":
        tracking_number = request.form["tracking_number"]
        package = Package.query.filter_by(tracking_number=tracking_number).first()
        if package:
            return render_template("package/track_result.html", package=package)
        else:
            flash("A megadott csomagszámmal nem található csomag.", "error")
    return render_template("package/track.html", title="Csomagkövetés")
