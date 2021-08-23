import flask_wtf
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import DateField

class LogginForm(flask_wtf.FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ")
    submit = SubmitField("Submit")


class NameCookie(flask_wtf.FlaskForm):
    name = StringField("Your name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NewPlanForm(flask_wtf.FlaskForm):
    name = StringField("Plan name", validators=[DataRequired()])
    submit = SubmitField("Add plan")


class NewPlanElement(flask_wtf.FlaskForm):
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')
    text = StringField("Text", validators=[DataRequired()])
    materials = StringField("Materials")
    submit = SubmitField("Add plan")