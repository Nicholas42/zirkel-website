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
