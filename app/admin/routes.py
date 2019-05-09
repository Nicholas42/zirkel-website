from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import User
from app.admin import bp
from app.decorators import role_required


@bp.before_request
@login_required
@role_required("admin")
def before_request():
    pass


@bp.route("/user_list")
def user_list():
    ul = User.query.all()

    return render_template("admin/user_list.html", user_list=ul)


@bp.route("/ban", methods=["POST"])
def ban():
    user_id = request.form["user"]
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()

    return redirect(url_for("admin.user_list"))
