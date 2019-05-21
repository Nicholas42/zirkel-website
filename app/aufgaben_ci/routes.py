from flask import current_app as app
from os import path
from app.aufgaben_ci import bp
from app.aufgaben_ci.helpers import pull_repo, make_all, copy_rec, PDF_PATTERN


@bp.route("/pullhook", methods=["POST", "GET"])
def pullhook():
    git_path = app.config["GIT_REPO"]
    origin_url = app.config["ORIGIN_URL"]
    pull_repo(git_path, origin_url)
    ret = make_all(git_path)
    copy_rec(git_path, path.join(bp.static_folder, "pdfs"), PDF_PATTERN)

    return "\n".join(["Done, %s runs, %s errors in:" % (ret[0], len(ret[1]))] + ret[1])
