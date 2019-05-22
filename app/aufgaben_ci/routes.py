from os import path, listdir

from flask import current_app as app, safe_join, abort, send_from_directory, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

from app.aufgaben_ci import bp
from app.aufgaben_ci.helpers import pull_repo, make_all, copy_rec, PDF_PATTERN
from app.decorators import role_required
from helpers import serve_path


@bp.route("/pullhook", methods=["POST", "GET"])
def pullhook():
    git_path = app.config["GIT_REPO"]
    origin_url = app.config["ORIGIN_URL"]
    pull_repo(git_path, origin_url)
    ret = make_all(git_path)
    copy_rec(git_path, path.join(bp.static_folder, "pdfs"), PDF_PATTERN)

    return "\n".join(["Done, %s runs, %s errors in:" % (ret[0], len(ret[1]))] + ret[1])


@bp.route("/project")
def serve_project():
    return send_from_directory(bp.static_folder, "pdfs/Organisatorisches/Projektbeschreibung.pdf")


@bp.route("/conventions")
@login_required
def serve_conventions():
    return send_from_directory(bp.static_folder, "pdfs/Technisches/Konventionen.pdf")


@bp.route("/tex/", defaults={"_path": "TeXTutorial"})
@bp.route("/tex/<path:_path>")
@login_required
def serve_tex(_path):
    return serve_path(_path, path.join(bp.static_folder, "pdfs", "Technisches"))


@bp.route("/modules/", defaults={"_path": ""})
@bp.route("/modules/<path:_path>")
@role_required("korrektor")
def serve_module(_path):
    return serve_path(_path, path.join(bp.static_folder, "pdfs"))
