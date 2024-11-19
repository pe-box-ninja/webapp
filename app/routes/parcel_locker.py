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
        "parcel_locker/parcel_lockers_list.html", title="Csomagautomaták", parcel_lockers=parcel_lockers
    )


@bp.route("parcel_locker/show_packages_inside_parcel_locker/<id>")
@login_required
@warehouse_required
def show_packages_inside_parcel_locker(id):
    
    status_filter = request.args.get("status", "all")
    search_query = request.args.get("search", "")

    query = Package.query

    if status_filter != "all":
        query = query.filter(Package.status == status_filter)

    if search_query:
        query = query.filter(
            or_(
                Package.tracking_number.ilike(f"%{search_query}%"),
                Package.sender_address.ilike(f"%{search_query}%"),
                Package.recipient_address.ilike(f"%{search_query}%"),
            )
        )

    packages = query.all()

    parcel_locker = ParcelLocker.query.get_or_404(id)
    assignments_query = Assignment.query
    assignments = assignments_query.all()


    parcel_locker_packages=[]

    for assignment in assignments:
        if assignment.parcel_locker_id==parcel_locker.id:
            package_id=assignment.package_id
            package=Package.query.get_or_404(package_id)
            if package.status != "kézbesítve":
                parcel_locker_packages.append(package)

    parcel_locker_package_with_search_and_status=[]

    intersectionset=set(packages).intersection(parcel_locker_packages)

    for item in intersectionset:
        parcel_locker_package_with_search_and_status.append(item)


    return render_template(
        "parcel_locker/show_packages_inside_parcel_locker.html", 
        title="Csomagautomatában lévő csomagok megtekintése", 
        parcel_locker=parcel_locker, 
        parcel_locker_package_with_search_and_status=parcel_locker_package_with_search_and_status,
        parcel_locker_package_with_search_and_status_length=len(parcel_locker_package_with_search_and_status),
        current_filter=status_filter,
        search_query=search_query,
        PackageStatus=PackageStatus
    )


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
    return render_template("parcel_locker/create.html", title="Új csomagautomata hozzáadása", form=form)


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
        "parcel_locker/edit.html", title="Csomagautomata szerkesztése", form=form, parcel_locker=parcel_locker
    )

