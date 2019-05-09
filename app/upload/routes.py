from flask import request, flash, redirect, url_for, render_template, current_app
from flask_login import login_required, current_user
from app import db, submissions
from app.upload import bp
from app.upload.forms import SubmissionForm
from app.models import Submission


@bp.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    print(current_app.upload_set_config["submissions"].tuple)
    form = SubmissionForm()
    if form.validate_on_submit():
        filename = submissions.save(request.files["file"])
        fileurl = submissions.url(filename)

        sub = Submission(author=current_user.id, notes=form.notes.data, filename=filename, fileurl=fileurl)
        db.session.add(sub)
        db.session.commit()

        flash("Bearbeitung erfolgreich hochgeladen.", category="success")
        return redirect(url_for("main.index"))

    return render_template("upload/submit.html", form=form)
