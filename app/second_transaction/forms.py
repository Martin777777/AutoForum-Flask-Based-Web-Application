from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, DateTimeField
from wtforms.validators import DataRequired, Length


class PublishCarForm(FlaskForm):
    name = StringField('Car Name', render_kw={"placeholder": "Car Name"},
                       validators=[DataRequired(), Length(1, 64)])
    link = StringField('Link', render_kw={"placeholder": "Link Address"}, validators=[DataRequired()])
    describe = TextAreaField('Car Describe', render_kw={"placeholder": "Car Describe"},
                             validators=[DataRequired()])
    chat = StringField('Contact Way', render_kw={"placeholder": "Contact Way"}, validators=[DataRequired()])
    mode = StringField('Transaction Mode', render_kw={"placeholder": "Transaction Mode"}, validators=[DataRequired()])
    photo = FileField('Car Show', validators=[DataRequired()])
    submit = SubmitField('Submit')
