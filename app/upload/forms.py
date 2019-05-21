from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField, DateField, TextField
from wtforms.validators import DataRequired


class SubmissionForm(FlaskForm):
    notes = TextAreaField("Anmerkungen")

    next_subject = TextField("Ich hätte gerne Aufgaben zum Thema", validators=[DataRequired()])
    next_module = DateField("am", format="%d.%m.%Y", validators=[DataRequired()])
    next_sub = DateField("und werde Bearbeitungen einreichen am", format="%d.%m.%Y", validators=[DataRequired()])
    file = FileField("Bearbeitung", validators=[DataRequired()])

    submit = SubmitField(label="Abschicken")

    def fields(self):
        yield self.notes
        yield self.file
