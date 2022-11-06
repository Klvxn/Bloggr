from flask import abort
from flask_login import current_user
from werkzeug.security import check_password_hash

from database.db import db
from users.models import User


def authorize(obj_owner, sus_user):
    """
    Checks that only the obj's owner is allowed to access the object.
    Return 403 forbidden if otherwise
    """
    user = db.get_or_404(User, sus_user.id)
    if obj_owner != user:
        return abort(403, "You don't have permission to perform this action")
    return True


def verify_password(email=None, password=..., use_current_user=False):
    """
    Verify a user against the provided password.
    Return the user object if the user exists and password is correct.
    """
    user = None
    if not use_current_user and email:
        user = db.session.query(User).filter(User.email == email).first()
    elif use_current_user:
        user = db.session.query(User).filter(User.id == current_user.id).first()
    if user and check_password_hash(user.password, password):
        return user
    return False
