from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Package

bp = Blueprint("package", __name__)


@bp.route("/list")
@login_required
def list():
    packages = Package.query.all()
    return render_template("package/list.html", title="Packages", packages=packages)


@bp.route("/view/<int:id>")
@login_required
def view(id):
    package = Package.query.get_or_404(id)
    return render_template("package/view.html", title="View Package", package=package)


@bp.route("/edit/<int:id>")
@login_required
def edit(id):
    package = Package.query.get_or_404(id)
    return render_template("package/edit.html", title="Edit Package", package=package)


@bp.route("/create")
@login_required
def create():
    return render_template("package/create.html", title="Create Package")
