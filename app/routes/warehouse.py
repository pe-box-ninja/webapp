from flask import Blueprint, render_template, flash
from flask_login import login_required
from app.models import Warehouse
from app.models import Assignment
from app.models import Package, PackageStatus
from app.decorators import warehouse_required

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
    return render_template(
        "warehouse/show_packages.html", title="Raktárban lévő csomagok megtekintése", warehouse=warehouse, warehouse_packages=warehouse_packages
    )
