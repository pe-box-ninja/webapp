from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from app.models import Warehouse
from app.models import Assignment
from app.models import Package, PackageStatus
from app.decorators import warehouse_required
from app.forms import EditWarehouseForm, CreateWarehouseForm
from app import db
from sqlalchemy import or_

bp = Blueprint("warehouse", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    warehouses = Warehouse.query.all()
    return render_template(
        "warehouse/warehouses_list.html", title="Raktárak", warehouses=warehouses
    )

@bp.route("warehouse/show_packages_inside_warehouse/<id>")
@login_required
@warehouse_required
def show_packages_inside_warehouse(id):
    
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

    warehouse = Warehouse.query.get_or_404(id)
    assignments_query = Assignment.query
    assignments = assignments_query.all()


    warehouse_packages=[]

    for assignment in assignments:
        if assignment.warehouse_id==warehouse.id:
            package_id=assignment.package_id
            package=Package.query.get_or_404(package_id)
            if package.status != "kézbesítve":
                warehouse_packages.append(package)

    warehouse_package_with_search_and_status=[]

    intersectionset=set(packages).intersection(warehouse_packages)

    for item in intersectionset:
        warehouse_package_with_search_and_status.append(item)


    return render_template(
        "warehouse/show_packages_inside_warehouse.html", 
        title="Raktárban lévő csomagok megtekintése", 
        warehouse=warehouse, 
        warehouse_package_with_search_and_status=warehouse_package_with_search_and_status,
        warehouse_package_with_search_and_status_length=len(warehouse_package_with_search_and_status),
        current_filter=status_filter,
        search_query=search_query,
        PackageStatus=PackageStatus
    )

@bp.route("/create", methods=["GET", "POST"])
@login_required
@warehouse_required
def create():
    form = CreateWarehouseForm()
    if form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            address=form.address.data,
            capacity=form.capacity.data,
            current_load=form.current_load.data,
        )
        db.session.add(warehouse)
        db.session.commit()
        flash("Sikeres raktárfelvétel!", "success")
        return redirect(url_for("warehouse.list"))
    return render_template("warehouse/create.html", title="Új raktár hozzáadása", form=form)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@warehouse_required
def edit(id):
    warehouse = Warehouse.query.get_or_404(id)
    form = EditWarehouseForm(obj=warehouse)
    if form.validate_on_submit():
        form.populate_obj(warehouse)
        db.session.commit()
        flash("A raktár sikeresen frissítve!", "success")
        return redirect(url_for("warehouse.list"))
    return render_template(
        "warehouse/edit.html", title="Raktár szerkesztése", form=form, warehouse=warehouse
    )

