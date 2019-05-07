from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


def validate_unique(column, error, table=User):
    def validator(form, field):
        if table.query.filter_by(**{column: field.data}).first() is not None:
            raise ValidationError(error)

    return validator


class LoginForm(FlaskForm):
    username = StringField(label="Benutzername", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    submit = SubmitField(label="Anmelden")

    def fields(self):
        yield self.username
        yield self.password


class RegistrationForm(FlaskForm):
    username = StringField(label="Benutzername",
                           validators=[DataRequired(), validate_unique("username", "Benutzername bereits vergeben,")])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password2 = PasswordField(label="Wiederhole Passwort", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(label="Anmelden")

    def fields(self):
        yield self.username
        yield self.password
        yield self.password2
