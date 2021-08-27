import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import DateField

class LogginForm(flask_wtf.FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ")
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")


class RegistrationForm(flask_wtf.FlaskForm):
    login = StringField("Login/email:", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat password: ", validators=[DataRequired()])
    registration_submit = SubmitField("Registration")


class NameCookieForm(flask_wtf.FlaskForm):
    name = StringField("Your name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NewPlanForm(flask_wtf.FlaskForm):
    name = StringField("Plan name", validators=[DataRequired()])
    submit = SubmitField("Add plan")


class NewPlanElementForm(flask_wtf.FlaskForm):
    date = DateField("Date")
    text = StringField("Text", validators=[DataRequired()])
    materials = StringField("Materials")
    submit = SubmitField("Add plan")


class NewNameForm(flask_wtf.FlaskForm):
    new_name = StringField("New name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")