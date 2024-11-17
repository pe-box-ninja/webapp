from flask import Blueprint, render_template, flash, request
from flask_login import login_required
from app.models import Warehouse
from app.models import Assignment
from app.models import Package, PackageStatus
from app.decorators import warehouse_required
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

@bp.route("warehouse/show_packages/<id>")
@login_required
@warehouse_required
def show_packages(id):
    
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
        "warehouse/show_packages.html", 
        title="Raktárban lévő csomagok megtekintése", 
        warehouse=warehouse, 
        warehouse_package_with_search_and_status=warehouse_package_with_search_and_status,
        warehouse_package_with_search_and_status_length=len(warehouse_package_with_search_and_status),
        current_filter=status_filter,
        search_query=search_query,
        PackageStatus=PackageStatus
    )
