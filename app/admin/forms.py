from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectMultipleField
from wtforms.validators import DataRequired, Email

from app.helpers.form_helpers import validate_unique
from app.models import Role


class CreateUserForm(FlaskForm):
    username = StringField(label="Benutzername",
                           validators=[DataRequired(), validate_unique("username", "Benutzername bereits vergeben,")])
    email = StringField(label="E-Mail", validators=[DataRequired(), Email(),
                                                    validate_unique("email", "E-Mail-Adresse bereits benutzt.")])
    roles = SelectMultipleField(label="Rollen", coerce=int)

    submit = SubmitField(label="Erstellen")

    def __init__(self, roles):
        super(CreateUserForm, self).__init__()
        self.roles.choices = [(i.id, i.name) for i in roles]
