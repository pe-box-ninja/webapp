from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('courier', __name__)

@bp.route('/list')
@login_required
def list():
    return render_template('courier/list.html', title='Couriers')