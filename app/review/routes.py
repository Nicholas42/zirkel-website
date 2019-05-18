from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from app import db, reviews
from app.decorators import role_required
from app.review import bp
from app.models import Submission, Review
from app.review.forms import ReviewUploadForm


@bp.before_request
@role_required("korrektor")
def before_request():
    pass


@bp.route("/submissions")
def submissions():
    return render_template("review/index.html", submissions=Submission.query.all())


@bp.route("/claim_submission", methods=["POST"])
def claim_submission():
    sub = Submission.query.get(request.form["sub_id"])
    sub.reviewer = current_user

    db.session.add(sub)
    db.session.commit()
    print(sub.reviewer)
    print(sub.is_claimed())

    return redirect(url_for("review.submissions"))


@bp.route("/review", methods=["GET", "POST"])
def review():
    form = ReviewUploadForm(submission_id=request.args.get("submission_id", None))
    if form.validate_on_submit():
        filename = reviews.save(request.files["review_file"])
        fileurl = reviews.url(filename)

        submission = Submission.query.get(form.submission_id.data)

        rev = Review(reviewer_id=current_user.get_id(), notes=form.notes.data, filename=filename, fileurl=fileurl)
        rev.submission = submission
        db.session.add(rev)
        db.session.commit()

        flash("Bewertung erfolgreich hochgeladen.", category="success")
        return redirect(url_for("review.submissions"))

    return render_template("review/review_form.html", form=form, title="Bewertung hochladen")
