from datetime import datetime

from database.db import db


class Blog(db.Model):

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False, index=True)
    content = db.Column(db.Text(5000), nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), default=datetime.now)
    tag = db.Column(db.String(80), nullable=True, index=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    comment = db.relationship("Comment", backref="comments")

    def __repr__(self):
        return f"{self.title} by {self.writer}"


class Comment(db.Model):

    id = db.Column(db.Integer, unique=True, primary_key=True)
    comment = db.Column(db.Text(800), nullable=False)
    blog = db.Column(
        db.Integer,
        db.ForeignKey("blog.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    guest_user = db.Column(db.String, nullable=True)
    date_posted = db.Column(db.DateTime(timezone=True), default=datetime.now)

    def __repr__(self):
        return f"{self.comment}"

    @staticmethod
    def add_comment(blog, comment, guest_user=None, user=None):
        new_comment = Comment(
            blog=blog.id, comment=comment, user=user, guest_user=guest_user
        )
        db.session.add(new_comment)
        db.session.commit()