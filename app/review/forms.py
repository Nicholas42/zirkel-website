from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import FileField, IntegerField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Submission, User
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
    module_path = StringField("Module", validators=[DataRequired()])
    user_name = SelectField("Benutzername", coerce=int)

    submit = SubmitField("Freigeben")

    def __init__(self):
        super(UnlockModuleForm, self).__init__()
        self.user_name.choices = [(i.id, i.username) for i in User.query.order_by(User.username)]
