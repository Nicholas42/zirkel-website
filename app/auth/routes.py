from flask import redirect, url_for, request, flash, render_template
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from app.email import send_password_reset
from app.helpers.route_helpers import safe_next
from app.models import User
from app.decorators import disable_route


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Bereits angemeldet", category="info")
        return redirect(safe_next(request.args.get("next")))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Benutzername oder Passwort ist falsch.", category="error")
            return redirect(url_for("auth.login"))

        if not login_user(user):
            flash("Dieser Benutzer ist deaktiviert. Bitte wende Dich an den Administrator.", category="error")
            return redirect(url_for("main.index"))

        flash("Erfolgreich angemeldet.", category="success")
        return redirect(safe_next(request.args.get("next")))

    return render_template("basic_form.html", title="Anmeldung", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Abgemeldet.", category="success")
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
@disable_route
def register():
    if current_user.is_authenticated:
        flash("Bereits angemeldet", category="info")
        return redirect(safe_next(request.args.get("next")))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, active=True)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Du bist jetzt registriert, %s!" % user.username, "success")
        return redirect(url_for("auth.login"))

    return render_template("basic_form.html", form=form, title="Registrierung")


@bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.npassword.data)

        db.session.commit()

        flash("Passwort erfolgreich geändert.", "success")

        return redirect(url_for("main.index"))

    return render_template("basic_form.html", form=form, title="Passwort ändern")


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("E-Mail nicht gefunden.", "error")
            return render_template("basic_form.html", title="Passwort vergessen", form=form)

        send_password_reset(user)
        flash("E-Mail versandt.")
        return redirect(url_for("auth.login"))

    return render_template("basic_form.html", title="Passwort vergessen", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.verify_reset_password_token(token)

    if not user:
        flash("Token nicht korrekt", "error")

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.npassword.data)
        db.session.commit()
        flash("Neues Passwort gesetzt", "success")

        return redirect(url_for("main.index"))

    return render_template("basic_form.html", title="Passwort-Reset", form=form)
