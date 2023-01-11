from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from database.db import db

from .forms import UserForm
from .models import User

users_bp = Blueprint("users", __name__, url_prefix="/users/")


@users_bp.route("/<int:user_id>/", methods=["GET", "POST"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("get_user.html", user=user)


@users_bp.route("/<int:user_id>/update_my_account/", methods=["GET", "POST"])
@login_required
def update_user_account(user_id):
    user = db.get_or_404(User, user_id)
    form = UserForm(obj=user)
    if user != current_user:
        return abort(403, "You do not have permission to perform this action.")
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.about = form.about.data
        db.session.commit()
        flash("Update was saved successfully", "success")
        return redirect(url_for(".get_user", user_id=user_id))
    context = {"form": form, "user": user}
    return render_template("update_user.html", **context)


@users_bp.route("/<int:user_id>/delete_account/", methods=["GET", "POST"])
@login_required
def delete_user_account(user_id):
    user = db.get_or_404(User, user_id)
    if user != current_user:
        return abort(403, "You do not have permission to perform this action.")
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        flash("Your account has been deleted", "warning")
        return redirect(url_for("blogs.home_page"))
    return render_template("delete_user.html", user=user)
