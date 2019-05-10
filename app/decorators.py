from flask import abort
from flask_login import current_user, login_required


def role_required(role):
    def decorator(f):
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role):
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator
