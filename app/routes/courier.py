from flask import Blueprint, render_template, flash, request
from flask_login import login_required
from flask import redirect, url_for
from app.models import Courier, CourierStatus, Package, PackageStatus, Assignment
from app import db
from app.decorators import warehouse_required
from app.forms import CreateCourierForm, EditCourierForm
from app.lib.algo import a_star_route_optimization
from app.lib.coordinates import get_coordinates
from flask_login import current_user
from tqdm import tqdm
from sqlalchemy import or_


bp = Blueprint("courier", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    couriers = Courier.query.all()
    status_filter = request.args.get("status", "all")
    return render_template("courier/list.html", title="Futárok", couriers=couriers)


@bp.route("/view/<int:id>")
@login_required
@warehouse_required
def view(id):
    courier = Courier.query.get_or_404(id)
    return render_template(
        "courier/view.html", title="Futár információk", courier=courier
    )


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@warehouse_required
def edit(id):
    courier = Courier.query.get_or_404(id)
    form = EditCourierForm(obj=courier)

    if form.validate_on_submit():
        form.populate_obj(courier)
        db.session.commit()
        flash("Courier updated successfully.", "success")
        return redirect(url_for("courier.list"))

    return render_template(
        "courier/edit.html", title="Futár módosítása", form=form, courier=courier
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
@warehouse_required
def create():
    form = CreateCourierForm()
    if form.validate_on_submit():
        courier = Courier(
            id=form.id.data,
            status=form.status.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            current_location=form.current_location.data,
            working_hours=form.working_hours.data,
            capacity=int(form.capacity.data),
            created_at=form.created_at.data,
            updated_at=form.updated_at.data,
        )
        db.session.add(courier)
        db.session.commit()
        flash("Futár regisztrálása!", "success")
        return redirect(url_for("courier.list"))
    return render_template("courier/create.html", title="Futár létrehozása", form=form)


@bp.route("/my_packages", methods=["GET", "POST"])
@login_required
@warehouse_required
def my_packages():
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

    courier = Courier.query.filter_by(id=current_user.id).first()
    assignments = (Assignment.query.filter_by(courier_id=courier.id).all())[:]
    packages = [
        p
        for p in (query.order_by(Package.weight.asc()).all())
        if p.id in [assignment.package_id for assignment in assignments]
    ]
    return render_template(
        "courier/my_packages.html",
        title="Csomagjaim",
        packages=packages,
        PackageStatus=PackageStatus,
    )


@bp.route("/assign_packages", methods=["GET", "POST"])
@login_required
@warehouse_required
def assign_packages():
    couriers = Courier.query.filter_by(status=CourierStatus.AVAILABLE).all()
    packages = (
        Package.query.filter_by(status=PackageStatus.PENDING)
        .order_by(Package.weight.asc())
        .all()
    )

    if not couriers:
        flash("Nincsenek elérhető futárok!", "warning")
        return redirect(url_for("courier.list"))

    if not packages:
        flash("Nincsenek kiosztásra váró csomagok!", "info")
        return redirect(url_for("package.list"))

    # Assignment logic
    assignments = []
    for courier in couriers:
        available_capacity = courier.capacity
        assigned_packages = []

        for package in packages[:]:
            if package.weight <= available_capacity:
                # Assign package to the courier
                assigned_packages.append(package)
                available_capacity -= package.weight
                package.status = PackageStatus.PENDING
                package.courier_id = courier.id

                packages.remove(package)

        assignments.append(
            {
                "courier": courier,
                "packages": assigned_packages,
            }
        )

    db.session.commit()

    flash("Csomagok sikeresen kiosztva a futároknak!", "success")

    return render_template(
        "courier/assign_packages.html",
        title="Csomagok felvétele",
        assignments=assignments,
    )


@bp.route("/optimal_path_api", methods=["GET", "POST"])
@login_required
@warehouse_required
def optimal_path_api():
    print("optimal_path_api")

    couriers = Courier.query.filter_by(status=CourierStatus.AVAILABLE).all()
    assignments = []
    bad_addresses = []

    addresses = [
        {
            "address": "Veszprém, Egyetem utca 10",
            "lat": get_coordinates("Veszprém, Egyetem utca 10")[0],
            "lon": get_coordinates("Veszprém, Egyetem utca 10")[1],
        }
    ]

    packages = Package.query.filter_by(status=PackageStatus.PENDING).all()

    for package in tqdm(packages, desc="Processing packages"):
        if package.recipient_address in bad_addresses:
            continue

        recipient_address = package.recipient_address
        lat, lon = get_coordinates(recipient_address)

        if lat is not None and lon is not None:
            addresses.append({"address": recipient_address, "lat": lat, "lon": lon})
        else:
            flash(
                f"Nem sikerült feldolgozni a következő címet: {recipient_address}",
                "warning",
            )
            bad_addresses.append(recipient_address)

    optimal_route, step_info = a_star_route_optimization(addresses, start_index=0)
    assignments.append(
        {"courier": Courier.name, "route": optimal_route, "steps": step_info}
    )

    return render_template(
        "courier/optimal_path.html",
        title="Optimális útvonal meghatározása",
        addresses=addresses,
        assignments=assignments,
    )


@bp.route("/optimal_path", methods=["GET"])
@login_required
@warehouse_required
def optimal_path():
    return render_template("courier/optimal_path_loading.html", title="Betöltés")
