from flask import render_template, redirect, url_for
from app.review import bp
from app.models import Submission


@bp.route("/submissions")
def submissions():
    return render_template("review/index.html", submissions=Submission.query.all())
