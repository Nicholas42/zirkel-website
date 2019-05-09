from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class SubmissionForm(FlaskForm):
    notes = TextAreaField("Anmerkungen")
    file = FileField("Bearbeitung", validators=[DataRequired()])

    submit = SubmitField(label="Abschicken")

    def fields(self):
        yield self.notes
        yield self.file
