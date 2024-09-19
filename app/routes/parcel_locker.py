from flask import Blueprint, render_template
from flask_login import login_required
from app.models import ParcelLocker
from app.decorators import warehouse_required

bp = Blueprint("parcel_locker", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    parcel_locker = ParcelLocker.query.all()
    return render_template(
        "parcel_locker/list.html", title="Csomagautomata", packages=parcel_locker
    )


@bp.route("/view/<int:id>")
@login_required
@warehouse_required
def view(id):
    parcel_locker = ParcelLocker.query.get_or_404(id)
    return render_template(
        "parcel_locker/view.html", title="Csomagautomata", package=parcel_locker
    )


@bp.route("/edit/<int:id>")
@login_required
@warehouse_required
def edit(id):
    parcel_locker = ParcelLocker.query.get_or_404(id)
    return render_template(
        "parcel_locker/edit.html",
        title="Csomagautomata módosítása",
        package=parcel_locker,
    )


@bp.route("/create")
@login_required
@warehouse_required
def create():
    return render_template(
        "parcel_locker/create.html", title="Csomagautomata felvétele"
    )
