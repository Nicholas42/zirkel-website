from flask import abort
from flask_login import current_user
from app.models import Role


def role_required(role):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not Role.query.filter_by(name=role).first() in current_user.roles:
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
