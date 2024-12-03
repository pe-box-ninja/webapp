from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.models import Package, PackageStatus, Warehouse, Assignment, ParcelLocker
from app.decorators import warehouse_required
from app import db
from app.forms import EditPackageForm, CreatePackageForm
from flask import redirect, url_for
from sqlalchemy import or_

bp = Blueprint("package", __name__)


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
            delivery_deadline=form.delivery_deadline.data,
        )
        db.session.add(package)
        db.session.commit()
        flash("Csomagküldés kezdeményezve!", "success")
        return redirect(url_for("package.list"))
    return render_template("package/create.html", title="Csomagküldés", form=form)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    status_filter = request.args.get("status", "all")
    search_query = request.args.get("search", "")
    warehouse_id = request.args.get("warehouse_id")
    parcel_locker_id = request.args.get("parcel_locker_id")

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

    warehouse = None
    parcel_locker = None

    if warehouse_id:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        query = query.join(Assignment).filter(
            Assignment.warehouse_id == warehouse_id, Package.status != "kézbesítve"
        )
    elif parcel_locker_id:
        parcel_locker = ParcelLocker.query.get_or_404(parcel_locker_id)
        query = query.join(Assignment).filter(
            Assignment.parcel_locker_id == parcel_locker_id,
            Package.status != "kézbesítve",
        )

    packages = query.all()

    return render_template(
        "package/list.html",
        title="Csomagok",
        packages=packages,
        current_filter=status_filter,
        search_query=search_query,
        PackageStatus=PackageStatus,
        warehouse_id=warehouse_id,
        warehouse=warehouse,
        parcel_locker_id=parcel_locker_id,
        parcel_locker=parcel_locker,
    )


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
