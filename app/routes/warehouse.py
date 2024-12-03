from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
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
        "warehouse/list.html",
        title="Raktárak",
        warehouses=warehouses,
        current_user=current_user,
    )


@bp.route("warehouse/list_packages/<id>")
@login_required
@warehouse_required
def list_packages(id: str):
    return redirect(url_for("package.list", warehouse_id=id))


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
    return render_template(
        "warehouse/create.html", title="Új raktár hozzáadása", form=form
    )


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
        "warehouse/edit.html",
        title="Raktár szerkesztése",
        form=form,
        warehouse=warehouse,
    )
