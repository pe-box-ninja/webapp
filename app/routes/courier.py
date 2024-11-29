from flask import Blueprint, render_template, flash, request
from flask_login import login_required
from flask import redirect, url_for
from app.models import Courier, CourierStatus
from app import db
from app.decorators import warehouse_required
from app.forms import CreateCourierForm, EditCourierForm

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
        status = form.status.data,
        name = form.name.data,
        email = form.email.data,
        phone = form.phone.data,
        current_location = form.current_location.data,
        working_hours = form.working_hours.data,
        capacity = int(form.capacity.data),
        created_at = form.created_at.data,
        updated_at = form.updated_at.data
        )
        db.session.add(courier)
        db.session.commit()
        flash("Futár regisztrálása!", "success")
        return redirect(url_for("courier.list"))
    return render_template("courier/create.html", title="Futár létrehozása", form=form)


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