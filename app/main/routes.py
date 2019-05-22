from flask import render_template
from app.main import bp


@bp.route("/")
@bp.route("/index.html")
def index():
    return render_template("main/index.html")


@bp.route("/contact")
def contact():
    return render_template("main/contact.html")
