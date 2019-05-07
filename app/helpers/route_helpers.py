from flask import url_for
from werkzeug.urls import url_parse


def safe_next(next_page, default="main.index"):
    if next_page is None or url_parse(next_page).netloc != "":
        return url_for(default)
    return next_page
