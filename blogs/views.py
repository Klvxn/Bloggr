from gettext import ngettext

from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from database.db import db

from .forms import BlogForm, CommentForm
from .models import Blog, Comment

blogs_bp = Blueprint("blogs", __name__)


@blogs_bp.route("/", methods=["GET"])
def home_page():
    blogs = db.session.query(Blog).order_by(Blog.date_posted.desc()).all()
    context = {"blogs": blogs, "user": current_user}
    query = request.args.get("search")
    if query:
        results = []
        message = "No blogs matched your search, Try typing something different"
        for blog in blogs:
            if query.lower() in blog.title.lower():
                results.append(blog)
                text = ngettext("result", "results", len(results))
                message = f"{len(results)} {text} found"
        flash(message, "info")
        context = {"blogs": results}
    return render_template("home_page.html", **context)


@blogs_bp.route("/blogs/<int:blog_id>/", methods=["GET", "POST"])
def get_single_blog(blog_id):
    blog = db.get_or_404(Blog, blog_id)
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data
        comment_as = form.comment_as.data
        if not current_user.is_authenticated and comment_as != "Guest":
            flash("You need to login to post a comment as a Member", "warning")
            return redirect(url_for("auth.log_in_user", next=f"/blogs/{blog_id}/"))
        elif comment_as == "Guest":
            Comment.add_comment(blog, comment, guest_user=name)
        else:
            Comment.add_comment(blog, comment, user_id=current_user.id)
        flash("Comment posted successfully", "success")
        return redirect(url_for(".get_single_blog", blog_id=blog_id))
    context = {"blog": blog, "form": form}
    return render_template("single_blog.html", **context)


@blogs_bp.route("/add_new_blog/", methods=["GET", "POST"])
@login_required
def add_blog():
    form = BlogForm()
    if form.validate_on_submit():
        new_blog = Blog()
        form.populate_obj(new_blog)
        new_blog.writer = current_user
        db.session.add(new_blog)
        db.session.commit()
        flash("Blog posted successfully", "success")
        return redirect(url_for(".home_page"))
    return render_template("add_blog.html", form=form)


@blogs_bp.route("/blogs/<int:blog_id>/edit_blog/", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    blog = db.get_or_404(Blog, blog_id)
    form = BlogForm(obj=blog)
    if blog.writer != current_user:
        return abort(403, "You don't have permission to perform this action")
    if form.validate_on_submit():
        form.populate_obj(blog)
        db.session.commit()
        flash("Update was saved successfully", "success")
        return redirect(url_for(".get_single_blog", blog_id=blog_id))
    context = {"blog": blog, "form": form}
    return render_template("edit_blog.html", **context)


@blogs_bp.route("/blogs/<int:blog_id>/delete_blog/", methods=["GET", "POST"])
@login_required
def delete_blog(blog_id):
    blog = db.get_or_404(Blog, blog_id)
    if blog.writer != current_user:
        return abort(403, "You don't have permission to perform this action")
    if request.method == "POST":
        db.session.delete(blog)
        db.session.commit()
        flash(f"Your blog has been deleted", "warning")
        return redirect(url_for(".home_page"))
    return render_template("delete_blog.html", blog=blog)
