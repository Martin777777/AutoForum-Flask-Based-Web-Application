from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class RegisterCompanyForm(FlaskForm):
    name = StringField('Firm Name', render_kw={"placeholder": "Firm Name"},
                       validators=[DataRequired(), Length(1, 64)])
    manager = StringField('Manager', render_kw={"placeholder": "Manager"},
                          validators=[DataRequired(), Length(1, 64)])
    email = StringField('Firm Email', render_kw={"placeholder": "Firm Email"},
                        validators=[DataRequired(), Length(1, 64), Email()])
    phone = StringField('Phone Number', render_kw={"placeholder": "Phone Number"},
                        validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit')


class PublishActivityForm(FlaskForm):
    name = StringField('Activity Name', render_kw={"placeholder": "Activity Name"},
                       validators=[DataRequired(), Length(1, 64)])
    time = DateTimeField("Activity Time", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    place = StringField('Activity Place', render_kw={"placeholder": "Activity Place"}, validators=[DataRequired()])
    describe = TextAreaField('Activity Describe', render_kw={"placeholder": "Activity Describe"},
                             validators=[DataRequired()])
    organizer = StringField('Activity Organizer', render_kw={"placeholder": "Activity Organizer"},
                            validators=[DataRequired()])
    photo = FileField('Auto Show', validators=[DataRequired()])
    submit = SubmitField('Submit')
