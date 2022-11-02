from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from database.db import db
from users.models import User


class RegisterForm(FlaskForm):

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    about = TextAreaField("About Yourself", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", "Passwords don't match"),
            Length(min=8),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    register = SubmitField("Register")

    def validate_email(self, field):
        """Check that the email is unique before processing the form data"""
        email_exists = db.session.query(User).filter(User.email == field.data).first()
        if email_exists:
            raise ValidationError("User with this email address already exists")


class LoginForm(FlaskForm):

    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    log_in = SubmitField("Log In")

    def validate_email(self, field):
        """Check that the email exists before processing the form data"""
        user = db.session.query(User).filter(User.email == field.data).first()
        if not user:
            raise ValidationError(f"No user with email address, {field.data}")


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password2", "Passwords don't match"),
            Length(min=8),
        ],
    )
    new_password2 = PasswordField("Confirm New Password", validators=[DataRequired()])
    change = SubmitField("Change Password")

    def validate_new_password(self, field):
        if field.data == self.old_password.data:
            raise ValidationError("New password cannot be the same as old password")
