from functools import wraps

from flask import abort, render_template
from flask_login import current_user, login_required


def role_required(role):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_role(role):
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def disable_route(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        return render_template("page_disabled.html"), 403

    return decorate_function
