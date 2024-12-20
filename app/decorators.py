from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def warehouse_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (
            not current_user.is_courier()
            and not current_user.is_warehouse()
            and not current_user.is_admin()
        ):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def courier_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (
            not current_user.is_warehouse() and not current_user.is_admin()
        ):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
