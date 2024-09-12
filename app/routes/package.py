from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('package', __name__)

@bp.route('/list')
@login_required
def list():
    return render_template('package/list.html', title='Packages')