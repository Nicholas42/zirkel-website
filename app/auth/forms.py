from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.helpers.form_helpers import validate_unique


class LoginForm(FlaskForm):
    username = StringField(label="Benutzername", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    submit = SubmitField(label="Anmelden")

    def fields(self):
        yield self.username
        yield self.password


class ChangePasswordForm(FlaskForm):
    password = PasswordField(label="Altes Passwort", validators=[DataRequired()])
    npassword = PasswordField(label="Neues Passwort", validators=[DataRequired()])
    npassword1 = PasswordField(label="Neues Passwort wiederholen", validators=[DataRequired(), EqualTo('npassword')])
    submit = SubmitField(label="Ändern")

    def validate_password(self, password):
        if not current_user.check_password(password.data):
            raise ValidationError("Passwort falsch")


class RegistrationForm(FlaskForm):
    username = StringField(label="Benutzername",
                           validators=[DataRequired(), validate_unique("username", "Benutzername bereits vergeben,")])
    email = StringField(label="E-Mail",
                        validators=[DataRequired(), Email(),
                                    validate_unique("email", "E-Mail-Adresse bereits benutzt.")])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password2 = PasswordField(label="Wiederhole Passwort", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(label="Anmelden")

    def fields(self):
        yield self.username
        yield self.email
        yield self.password
        yield self.password2
