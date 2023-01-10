from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    about = TextAreaField("About Yourself", validators=[DataRequired()])
    submit = SubmitField("Update")


class ContactForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")
