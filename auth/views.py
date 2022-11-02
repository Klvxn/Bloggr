from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import db
from users.models import User
from utils import validate_user

from .forms import LoginForm, ChangePasswordForm, RegisterForm

auth_bp = Blueprint("auth", __name__, template_folder="templates/", url_prefix="/auth/")


@auth_bp.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = form.password.data
        form.password.data = generate_password_hash(password)
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registration was successful", "success")
        return redirect(url_for("blogs.home_page"))
    return render_template("register.html", form=form)


@auth_bp.route("/log_in/", methods=["GET", "POST"])
def log_in_user():
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        valid_user = validate_user(email, password)
        if not valid_user:
            flash("Invalid email or password", "error")
        else:
            login_user(valid_user)
            next_url = request.args.get("next")
            if next_url:
                return redirect(next_url)
            flash("You are logged in successfully", "success")
            return redirect(url_for("blogs.home_page"))
    return render_template("log_in.html", form=form)


@auth_bp.route("/log_out/", methods=["GET", "POST"])
def log_out_user():
    if request.method == "POST":
        logout_user()
        flash("You are now logged out", "warning")
        return redirect(url_for("blogs.home_page"))
    return render_template("log_out.html")


@auth_bp.route("/change_password/", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pwd = form.old_password.data
        new_pwd = form.new_password.data
        valid_user = validate_user(password=old_pwd, use_current_user=True)
        if not valid_user:
            flash("Password is not correct", "error")
        else:
            valid_user.password = generate_password_hash(new_pwd)
            db.session.commit()
            flash("Password changed succesfully", "success")
            return redirect(url_for("users.get_user", user_id=current_user.id))
    return render_template("change_password.html", form=form)
