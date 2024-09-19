from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Warehouse
from app.decorators import warehouse_required

bp = Blueprint("warehouse", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    warehouses = Warehouse.query.all()
    return render_template(
        "warehouse/list.html", title="Warehouses", warehouses=warehouses
    )
