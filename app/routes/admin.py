from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app.models import User
from app.decorators import admin_required
import json
from app import db
from app.models import Package, Courier, Warehouse, Assignment, ParcelLocker


bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template("admin/index.html", title="Admin Kezelőpult", users=users)


@bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template("admin/users.html", title="Felhasználó kezelés", users=users)


@bp.route("/admin/change_permission", methods=["POST"])
@login_required
@admin_required
def change_permission():
    data = json.loads(request.data)
    userId = data["userId"]
    new_permission = data["new_permission"]
    user = User.query.get(userId)
    print(userId, new_permission)

    user.role = new_permission
    db.session.add(user)
    db.session.commit()


@bp.route("/db")
@login_required
@admin_required
def db_view():
    users = User.query.all()
    packages = Package.query.all()
    couriers = Courier.query.all()
    warehouses = Warehouse.query.all()
    assignments = Assignment.query.all()
    parcel_lockers = ParcelLocker.query.all()

    return render_template(
        "admin/db.html",
        title="Database Overview",
        users=users,
        packages=packages,
        couriers=couriers,
        warehouses=warehouses,
        assignments=assignments,
        parcel_lockers=parcel_lockers,
    )
