from os import path, listdir

from flask import current_app as app, safe_join, abort, send_from_directory, render_template
from werkzeug.exceptions import NotFound

from app.aufgaben_ci import bp
from app.aufgaben_ci.helpers import pull_repo, make_all, copy_rec, PDF_PATTERN
from app.decorators import role_required


@bp.route("/pullhook", methods=["POST", "GET"])
def pullhook():
    git_path = app.config["GIT_REPO"]
    origin_url = app.config["ORIGIN_URL"]
    pull_repo(git_path, origin_url)
    ret = make_all(git_path)
    copy_rec(git_path, path.join(bp.static_folder, "pdfs"), PDF_PATTERN)

    return "\n".join(["Done, %s runs, %s errors in:" % (ret[0], len(ret[1]))] + ret[1])


@bp.route("/modules", defaults={"_path": ""})
@bp.route("/modules/<path:_path>")
@role_required("korrektor")
def serve_module(_path):
    try:
        p = safe_join(bp.static_folder, "pdfs", _path)
    except NotFound:
        print(_path)
        abort(404)

    if path.isdir(p):
        children = []
        for i in listdir(p):
            children.append({"name": i, "path": path.join(_path, i)})
        return render_template("aufgaben_ci/modules.html", title=path.basename(p), children=children)
    elif path.isfile(p):
        print("sending")
        return send_from_directory(path.join(bp.static_folder, "pdfs"), _path)
    else:
        print()
        abort(404)
