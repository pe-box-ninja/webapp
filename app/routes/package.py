from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('package', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')