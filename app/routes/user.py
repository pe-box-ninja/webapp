from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('user', __name__)

@bp.route('/list')
@login_required
def list():
    return render_template('user/list.html', title='Users')