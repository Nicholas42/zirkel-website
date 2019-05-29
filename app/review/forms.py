from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.fields import FileField, IntegerField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, ValidationError
from app.models import Submission
from app.helpers.form_helpers import validate_exists


class ReviewUploadForm(FlaskForm):
    submission_id = IntegerField("Bearbeitungsid", validators=[DataRequired(),
                                                               validate_exists("id", "Bearbeitung existiert nicht.",
                                                                               Submission)])
    points = FloatField("Punkte", validators=[DataRequired()])
    notes = TextAreaField("Anmerkungen (privat)")
    review_file = FileField("Bewertungsdatei", validators=[DataRequired()])

    submit = SubmitField("Abschicken")

    def validate_submission_id(self, field):
        if Submission.query.get(field.data) is None:
            raise ValidationError("Bearbeitungsid existiert nicht.")


class UnlockModuleForm(FlaskForm):
    module_path = TextField("Module", validators=[DataRequired()])
    user_name = TextField("Benutzername",
                          validators=[DataRequired(), validate_exists("username", "Benutzer existiert nicht.")])

    submit = SubmitField("Freigeben")
