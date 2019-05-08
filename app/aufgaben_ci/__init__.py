from flask import Blueprint
from flask_login import login_required

bp = Blueprint("aufgaben_ci", __name__, static_folder="static")

from app.aufgaben_ci import routes
