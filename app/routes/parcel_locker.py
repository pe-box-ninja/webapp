from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import ParcelLocker, Package, Assignment, PackageStatus
from app.decorators import warehouse_required
from sqlalchemy import or_

bp = Blueprint("parcel_locker", __name__)


@bp.route("/view/<int:id>")
@login_required
@warehouse_required
def view(id):
    parcel_locker = ParcelLocker.query.get_or_404(id)
    return render_template(
        "parcel_locker/view.html", title="Csomagautomata", parcel_locker=parcel_locker
    )


@bp.route("/edit/<int:id>")
@login_required
@warehouse_required
def edit(id):
    parcel_locker = ParcelLocker.query.get_or_404(id)
    return render_template(
        "parcel_locker/edit.html",
        title="Csomagautomata módosítása",
        parcel_locker=parcel_locker,
    )


@bp.route("/create")
@login_required
@warehouse_required
def create():
    return render_template(
        "parcel_locker/create.html", title="Csomagautomata felvétele"
    )


@bp.route("/list")
@login_required
@warehouse_required
def list():
    parcel_lockers = ParcelLocker.query.all()
    return render_template(
        "parcel_locker/parcel_lockers_list.html", title="Csomagautomaták", parcel_lockers=parcel_lockers
    )


@bp.route("parcel_locker/show_packages_inside_parcer_locker/<id>")
@login_required
@warehouse_required
def show_packages_inside_parcer_locker(id):
    
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