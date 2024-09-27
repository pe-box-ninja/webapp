from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.models import Package
from app.decorators import warehouse_required
from app import db
from app.forms import EditPackageForm, CreatePackageForm
from flask import redirect, url_for

bp = Blueprint("package", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    packages = Package.query.all()
    return render_template("package/list.html", title="Csomagok", packages=packages)


@bp.route("/view/<int:id>")
@login_required
def view(id):
    package = Package.query.get_or_404(id)
    return render_template(
        "package/track_result.html", title="Csomagkövetés", package=package
    )


@bp.route("/send")
@login_required
def send():
    return render_template("package/send.html", title="Csomagküldés")


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


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@warehouse_required
def edit(id):
    package = Package.query.get_or_404(id)
    form = EditPackageForm(obj=package)
    if form.validate_on_submit():
        form.populate_obj(package)
        db.session.commit()
        flash("A csomag sikeresen frissítve.", "success")
        return redirect(url_for("package.list"))
    return render_template(
        "package/edit.html", title="Csomag szerkesztése", form=form, package=package
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
@warehouse_required
def create():
    form = CreatePackageForm()
    if form.validate_on_submit():
        package = Package(
            tracking_number=form.tracking_number.data,
            status=form.status.data,
            weight=form.weight.data,
            dimensions=form.dimensions.data,
            sender_address=form.sender_address.data,
            recipient_address=form.recipient_address.data,
        )
        db.session.add(package)
        db.session.commit()
        flash("Az új csomag sikeresen létrehozva.", "success")
        return redirect(url_for("package.list"))
    return render_template(
        "package/create.html", title="Új csomag létrehozása", form=form
    )
