from flask import request, flash, redirect, url_for, render_template, send_from_directory, abort, current_app
from flask_login import login_required, current_user

from app import db, submissions
from app.models import Submission
from app.upload import bp
from app.upload.forms import SubmissionForm
from app.decorators import role_required


@bp.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    form = SubmissionForm()
    if form.validate_on_submit():
        filename = submissions.save(request.files["file"])
        fileurl = submissions.url(filename)

        sub = Submission(author_id=current_user.get_id(), notes=form.notes.data, filename=filename, fileurl=fileurl)

        current_user.next_module = form.next_module.data
        current_user.next_sub = form.next_sub.data
        current_user.next_subject = form.next_subject.data

        db.session.add(sub)
        db.session.commit()

        flash("Bearbeitung erfolgreich hochgeladen.", category="success")
        return redirect(url_for("main.index"))

    return render_template("upload/submit.html", form=form)


@bp.route("/uploads/submissions/<filename>")
@role_required("korrektor")
def serve_file(filename):
    if Submission.query.filter_by(filename=filename).first() is None:
        abort(404)

    return send_from_directory(submissions.config.destination, filename)


@bp.route("/submission/<int:index>")
def submission(index):
    sub = Submission.query.get(index)
    if sub is None:
        abort(404)

    if not current_user.has_role("korrektor") and not sub.author == current_user:
        abort(403)

    return render_template("upload/submission.html", sub=sub)


@bp.route("/my_submissions")
@login_required
def my_submissions():
    subs = Submission.query.filter_by(author_id=current_user.id)

    return render_template("upload/my_submissions.html", subs=subs)
