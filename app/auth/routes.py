from flask import redirect, url_for, request, flash, render_template
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return "Bereits angemeldet."

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Benutzername oder Passwort ist falsch.", category="error")
            return redirect(url_for("auth.login"))

        login_user(user)

        next_page = request.args.get("next")
        if next_page is None or url_parse(next_page).netloc != "":
            # Zweiteres ist gegen Weiterleitungen außerhalb der Seite
            next_page = url_for("main.index")

        flash("Erfolgreich angemeldet.", category="success")
        return redirect(next_page)

    return render_template("auth/login.html", title="Anmeldung", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Abgemeldet.", category="success")
    return redirect(url_for("main.index"))
