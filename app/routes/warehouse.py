from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Warehouse

bp = Blueprint("warehouse", __name__)


@bp.route("/list")
@login_required
def list():
    warehouses = Warehouse.query.all()
    return render_template("warehouse/list.html", title="Raktárak", packages=warehouses)


@bp.route("/view/<int:id>")
@login_required
def view(id):
    warehouse = Warehouse.query.get_or_404(id)
    return render_template("warehouse/view.html", title="Raktár", package=warehouse)


@bp.route("/edit/<int:id>")
@login_required
def edit(id):
    warehouse = Warehouse.query.get_or_404(id)
    return render_template(
        "warehouse/edit.html", title="Raktár szerkesztése", package=warehouse
    )


@bp.route("/create")
@login_required
def create():
    return render_template("warehouse/create.html", title="Raktár felvitele")
