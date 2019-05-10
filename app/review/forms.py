from flask_wtf import FlaskForm
from wtforms.fields import FileField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import Submission


class ReviewUploadForm(FlaskForm):
    submission_id = IntegerField("Bearbeitungsid", validators=[DataRequired()])
    notes = TextAreaField("Anmerkungen (privat)")
    review_file = FileField("Bewertungsdatei", validators=[DataRequired()])

    submit = SubmitField("Abschicken")

    def validate_submission_id(self, field):
        if Submission.query.get(field.data) is None:
            raise ValidationError("Bearbeitungsid existiert nicht.")
