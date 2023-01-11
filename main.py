from flask import Flask, flash, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail, Message

import app_conf
from auth.views import auth_bp
from blogs.views import blogs_bp
from blogs.models import Blog, Comment
from database.db import db
from users.forms import ContactForm
from users.models import User
from users.views import users_bp

app = Flask(__name__)
app.config.from_object(app_conf)
app.register_blueprint(auth_bp)
app.register_blueprint(blogs_bp)
app.register_blueprint(users_bp)

bootstrap = Bootstrap5(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.log_in_user"
login_manager.login_message_category = "warning"


mail = Mail(app)
mail.init_app(app)


@app.before_first_request
def create_database():
    db.create_all()


@app.route("/about/", methods=["GET"])
def about_page():
    return render_template("about_page.html")


@app.route("/contact-us/", methods=["GET", "POST"])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = Message(
            subject="Greetings",
            recipients=["akpulukelvin@gmail.com"],
            body=message,
            sender=(name, email),
        )
        mail.connect()
        mail.send(msg)
        flash(
            "Your message was sent successfully. We'd get back to you as soon as possible",
            "success",
        )
        return redirect("/contact-us/")
    return render_template("contact_page.html", form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
