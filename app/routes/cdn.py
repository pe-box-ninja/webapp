from flask import Blueprint, send_file, current_app
import os

bp = Blueprint("cdn", __name__)


@bp.route("/logo", methods=["GET"])
def serve_logo():
    logo_path = os.path.join(current_app.root_path, "static", "icon-tp.png")
    return send_file(logo_path, mimetype="image/png")
