from os import path

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user

from app import db, reviews
from app.decorators import role_required
from app.review import bp
from app.models import Submission, Review, Module, User
from app.review.forms import ReviewUploadForm, UnlockModuleForm


@bp.before_request
@role_required("korrektor")
def before_request():
    pass


@bp.route("/submissions")
def submissions():
    all_subs = Submission.query.all()
    active = filter(lambda x: not x.is_claimed() and x.is_open(), all_subs)
    under_review = filter(lambda x: x.is_claimed() and x.is_open(), all_subs)
    closed = filter(lambda x: not x.is_open(), all_subs)
    return render_template("review/index.html", active=active, under_review=under_review, closed=closed)


@bp.route("/claim_submission")
def claim_submission():
    sub = Submission.query.get_or_404(request.args.get("sub_id"))

    sub.reviewer = current_user;

    db.session.add(sub)
    db.session.commit()

    return redirect(url_for("review.submissions"))


@bp.route("/review", methods=["GET", "POST"])
def review():
    form = ReviewUploadForm(submission_id=request.args.get("sub_id", None))
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


@bp.route("/unlock_module", methods=["GET", "POST"])
def unlock_module():
    form = UnlockModuleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user_name.data).first()
        if user is None:
            flash("Benutzer existiert nicht", "error")
            return render_template("basic_form.html", title="Modul freigeben", form=form)

        mod = Module.query.filter_by(path=form.module_path.data).first()
        if mod is None:
            mod = Module(path=form.module_path.data)

        mod.permitted_users.append(user)
        db.session.add(mod)
        db.session.commit()

        flash("Module freigegeben")
        return redirect(path.dirname(mod.path))

    form.module_path.data = request.args.get("module_path", "")

    return render_template("basic_form.html", title="Modul freigeben", form=form)


@bp.route("/user_list")
def user_list():
    all_users = User.query.all()

    return render_template("review/user_list.html", all_users=all_users)


@bp.route("/show_user/<uid>")
def show_user(uid):
    user = User.query.get_or_404(uid)

    return render_template("review/show_user.html", user=user)
