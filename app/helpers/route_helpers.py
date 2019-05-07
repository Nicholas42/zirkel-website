from flask import url_for
from werkzeug.urls import url_parse


def safe_next(next, default="main.index"):
    if next is None or url_parse(next).netloc != "":
        return url_for(default)
    return next
