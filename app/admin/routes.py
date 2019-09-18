from flask import render_template, request, redirect, url_for, flash, current_app
from os import remove, path
from app import db, submissions
from app.email import send_mail
from app.admin.forms import CreateUserForm
from app.models import User, Role, Submission
from app.admin import bp
from app.decorators import role_required
from app.helpers.route_helpers import safe_next


@bp.before_request
@role_required("admin")
def before_request():
    pass


@bp.route("/")
@bp.route("/panel")
def panel():
    return render_template("admin/panel.html")


@bp.route("/user_list")
def user_list():
    ul = User.query.all()

    return render_template("admin/user_list.html", user_list=ul, role_list=Role.query.all())


@bp.route("/ban", methods=["POST"])
def ban():
    user_id = request.form["user"]
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()

    return redirect(url_for("admin.user_list"))


@bp.route("/add_role", methods=["POST"])
def add_role():
    user_id = request.form["user_id"]
    user = User.query.get(user_id)
    user.roles.append(Role.query.get(request.form["role_id"]))
    db.session.commit()

    return redirect(url_for("admin.user_list"))


@bp.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm(Role.query.all())
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    roles=[Role.query.get(i) for i in form.roles.data])
        pw = user.set_random_password()

        db.session.add(user)
        db.session.commit()

        send_mail("Anmeldung beim Korrespondenzzirkel",
                  render_template("email/create_user.txt", password = pw, user = user, admin_mail = current_app.config["ADMIN_MAIL"]),
                  [user.email])

        return redirect(url_for("admin.create_user"))

    return render_template("basic_form.html", form=form, title="Erstelle Benutzer")


@bp.route("/delete_submission")
def delete_submission():
    submission = Submission.query.get_or_404(request.args.get("sub_id", None))

    if submission is None:
        flash("Bearbeitungsid nicht vorhanden.", "error")
        return redirect(safe_next(request.args.get("next")))

    try:
        remove(path.join(submissions.config.destination, submission.filename))
    except FileNotFoundError:
        flash("Datei war bereits gelöscht.")

    db.session.delete(submission)
    db.session.commit()

    flash("Bearbeitung entfernt.", "success")
    return redirect(safe_next(request.args.get("next"), default="review.submissions"))
