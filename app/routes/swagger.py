from flask import Blueprint, send_from_directory
import os

bp = Blueprint("swagger", __name__)


@bp.route("/swagger.json")
def swagger():
    return send_from_directory("static", "swagger.json")
