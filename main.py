from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import app_conf
from auth.views import auth_bp
from blogs.models import Blog
from blogs.views import blogs_bp
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

migrate = Migrate(app, db, "database/migrations/")


@app.before_first_request
def create_database():
    db.create_all()


@app.route("/about/", methods=["GET"])
def about_page():
    return render_template("about_page.html")


@app.route("/contact-us/", methods=["GET"])
def contact_page():
    form = ContactForm()
    return render_template("contact_page.html", form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
