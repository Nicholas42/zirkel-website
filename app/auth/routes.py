from flask import redirect, url_for, request, flash, render_template
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.helpers.route_helpers import safe_next
from app.models import User


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

        login_user(user)

        flash("Erfolgreich angemeldet.", category="success")
        return redirect(safe_next(request.args.get("next")))

    return render_template("auth/login.html", title="Anmeldung", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Abgemeldet.", category="success")
    return redirect(url_for("main.index"))
