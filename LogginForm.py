import flask_wtf
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LogginForm(flask_wtf.FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ")
    submit = SubmitField("Submit")