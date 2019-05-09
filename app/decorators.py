from flask import abort
from flask_login import current_user
from app import db
from app.models import Role, user_roles


def role_required(role):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            user_id = current_user.id
            role_id = Role.query.filter_by(name=role).first().id

            if db.session.query(user_roles).filter_by(user_id=user_id, role_id=role_id).first() is None:
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
