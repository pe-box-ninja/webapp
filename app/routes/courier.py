from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Courier
from app import db
from app.decorators import warehouse_required

bp = Blueprint("courier", __name__)


@bp.route("/list")
@login_required
@warehouse_required
def list():
    couriers = Courier.query.all()
    return render_template("courier/list.html", title="Futárok", couriers=couriers)


@bp.route("/view/<int:id>")
@login_required
@warehouse_required
def view(id):
    courier = Courier.query.get_or_404(id)
    return render_template(
        "courier/view.html", title="Futár információk", courier=courier
    )


@bp.route("/edit/<int:id>")
@login_required
@warehouse_required
def edit(id):
    courier = Courier.query.get_or_404(id)
    return render_template(
        "courier/edit.html", title="Futár módosítása", courier=courier
    )


@bp.route("/create")
@login_required
@warehouse_required
def create():
    return render_template("courier/create.html", title="Futár létrehozása")


@bp.route("/assign_packages")
@login_required
@warehouse_required
def assign_packages():
    return render_template("courier/assign_packages.html", title="Csomagok felvétele")


@bp.route("/optimat_path")
@login_required
@warehouse_required
def optimal_path():
    return render_template("courier/optimal_path.html", title="Optimális útvonal meghatározása")