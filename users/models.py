from flask_login import UserMixin

from blogs.models import Blog, Comment
from database.db import db


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    about = db.Column(db.Text(100), nullable=False)
    socials = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(50), unique=True, nullable=False)
    blogs = db.relationship(Blog, backref="writer", lazy=True)
    comments = db.relationship(Comment, backref="posted_by", lazy=True)

    def __repr__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"