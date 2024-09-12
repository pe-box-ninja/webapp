from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('warehouse', __name__)

@bp.route('/list')
@login_required
def list():
    return render_template('warehouse/list.html', title='Warehouses')