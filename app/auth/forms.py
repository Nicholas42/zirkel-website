from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


def validate_unique(column, data, error, table=User):
    if table.query.filter_by(**{column: data}).first() is not None:
        raise ValidationError(error)


class LoginForm(FlaskForm):
    username = StringField(label="Benutzername", validators=[DataRequired])
    password = PasswordField(label="Passwort", validators=[DataRequired])
    submit = SubmitField(label="Anmelden")


class RegistrationForm(LoginForm):
    password2 = PasswordField(label="Wiederhole Passwort", validators=[DataRequired, EqualTo('password')])

    def validate_username(self, username):
        return validate_unique("username", username.data, "Benutzername bereits vergeben.")

    def validate_email(self, email):
        return validate_unique("email", email.data, "E-Mail-Adresse wird bereits benutzt.")
