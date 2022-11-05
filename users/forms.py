from flask_wtf import FlaskForm
from wtforms import (EmailField, Form, FormField, RadioField, StringField,
                     SubmitField, TextAreaField, URLField)
from wtforms.validators import DataRequired, Email


class SocialsForm(Form):

    social = RadioField(
        "",
        validators=[DataRequired()],
        choices=("Twitter", "LinkedIn", "GitHub"),
    )
    network_url = URLField(
        "",
        validators=[DataRequired()],
        render_kw={"placeholder": "URL to your profile"},
    )


class UserForm(FlaskForm):

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    socials = FormField(SocialsForm, "Social")
    about = TextAreaField("About Yourself", validators=[DataRequired()])
    submit = SubmitField("Update")


class ContactForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")
