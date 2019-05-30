import shutil
from os import path

from flask import current_app as app, send_from_directory
from flask_login import login_required

from app.aufgaben_ci import bp
from app.aufgaben_ci.helpers import pull_repo, make_all, copy_rec, serve_path, tex_to_pdf, TEX_PATTERN


@bp.route("/pullhook", methods=["POST", "GET"])
def pullhook():
    git_path = app.config["GIT_REPO"]
    origin_url = app.config["ORIGIN_URL"]
    target_path = path.join(bp.static_folder, "pdfs")

    pull_repo(git_path, origin_url)
    ret = make_all(git_path)

    shutil.rmtree(target_path)
    copy_rec(git_path, target_path, TEX_PATTERN, tex_to_pdf)
    copy_rec(git_path, target_path, "**/beispiel.tex")

    return "\n".join(["Done, %s runs, %s errors in:" % (ret[0], len(ret[1]))] + ret[1])


@bp.route("/project")
def serve_project():
    return send_from_directory(bp.static_folder, "pdfs/Organisatorisches/Projektbeschreibung.pdf")


@bp.route("/conventions")
@login_required
def serve_conventions():
    return send_from_directory(bp.static_folder, "pdfs/Technisches/Konventionen.pdf")


@bp.route("/tex/", defaults={"_path": ""})
@bp.route("/tex/<path:_path>")
@login_required
def serve_tex(_path):
    return serve_path(_path, path.join(bp.static_folder, "pdfs", "Technisches", "TeXTutorial"), "TeX-Tutorial",
                      ignore_access=True)


@bp.route("/modules/", defaults={"_path": ""})
@bp.route("/modules/<path:_path>")
def serve_module(_path):
    return serve_path(_path, path.join(bp.static_folder, "pdfs", "Inhaltliches"), "Module")
