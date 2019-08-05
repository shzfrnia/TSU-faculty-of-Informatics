from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, TextField
from wtforms.validators import DataRequired, Length


class TranslateForm(FlaskForm):
    to_language = TextField("Choose language", validators=[DataRequired()])
    input_text = TextAreaField("Input", validators=[DataRequired()])
    output_field = TextAreaField("Outpup")
    submit = SubmitField("Translate!")
