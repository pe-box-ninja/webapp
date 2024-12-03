from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from app.models import ParcelLocker, Package, Assignment, PackageStatus
from app.decorators import warehouse_required
from app.forms import EditParcelLockerForm, CreateParcelLockerForm
from app import db
from sqlalchemy import or_

bp = Blueprint("parcel_locker", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    parcel_lockers = ParcelLocker.query.all()
    return render_template(
        "parcel_locker/parcel_lockers_list.html",
        title="Csomagautomaták",
        parcel_lockers=parcel_lockers,
    )


@bp.route("parcel_locker/list_packages/<id>")
@login_required
@warehouse_required
def list_packages(id):
    return redirect(url_for("package.list", parcel_locker_id=id))


@bp.route("/create", methods=["GET", "POST"])
@login_required
@warehouse_required
def create():
    form = CreateParcelLockerForm()
    if form.validate_on_submit():
        parcel_locker = ParcelLocker(
            location=form.location.data,
            address=form.address.data,
            total_compartments=form.total_compartments.data,
            available_compartments=form.available_compartments.data,
        )
        db.session.add(parcel_locker)
        db.session.commit()
        flash("Sikeres csomagautomatafelvétel!", "success")
        return redirect(url_for("parcel_locker.list"))
    return render_template(
        "parcel_locker/create.html", title="Új csomagautomata hozzáadása", form=form
    )


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@warehouse_required
def edit(id):
    parcel_locker = ParcelLocker.query.get_or_404(id)
    form = EditParcelLockerForm(obj=parcel_locker)
    if form.validate_on_submit():
        form.populate_obj(parcel_locker)
        db.session.commit()
        flash("A csomagautomata sikeresen frissítve!", "success")
        return redirect(url_for("parcel_locker.list"))
    return render_template(
        "parcel_locker/edit.html",
        title="Csomagautomata szerkesztése",
        form=form,
        parcel_locker=parcel_locker,
    )
