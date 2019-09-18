import os
from os import path, listdir
from urllib import request

from flask import safe_join, render_template, send_from_directory, abort, url_for, request
from flask_login import current_user
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from shutil import copy
from subprocess import run, DEVNULL
from pathlib import Path

from werkzeug.exceptions import NotFound

from app.aufgaben_ci import bp

LATEXMK_CALL = ["latexmk", "-cd", "-norc", "-pdf", "-quiet"]
ALL_PATTERN = "**/*"
PDF_PATTERN = "**/*.pdf"
TEX_PATTERN = "**/*.tex"


def url_to_path(url):
    if not url.startswith(bp.url_prefix):
        return None

    url = url[len(bp.url_prefix):]

    if url.startswith("/modules/"):
        return safe_join(path.join(bp.static_folder, "pdfs", "Inhaltliches"), url[len("/modules/"):])
    elif url.startswith("/tex/"):
        return safe_join(path.join(bp.static_folder, "pdfs", "Technisches", "TeXTutorial"), url[len("/modules/"):])

    return None


def pull_repo(git_path, upstream_url):
    try:
        repo = Repo(git_path)
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.clone_from(upstream_url, git_path, branch="release")

    repo.git.pull()


def make_all(directory):
    directory = Path(directory)
    runs = 0
    errors = []
    env = os.environ.copy()
    env["TEXMFHOME"] = str(directory.joinpath("Technisches/texmf"))
    for f in directory.glob("**/*.tex"):
        runs += 1
        ret = run(LATEXMK_CALL + [str(f.absolute())], env=env, stdout=DEVNULL, stderr=DEVNULL,
                  cwd=str(f.parent.absolute()))
        if ret.returncode != 0:
            errors.append(str(f.relative_to(directory)))

    return runs, errors


def tex_to_pdf(f):
    if f.is_file():
        assert (f.suffix == ".tex")

        return f.with_suffix(".pdf")

    return f


def copy_rec(source, target, allowed=ALL_PATTERN, transform=lambda x: x):
    source = Path(source)
    target = Path(target)
    for f in source.glob(allowed):
        f = transform(f)
        rel_target = target.joinpath(f.relative_to(source))
        if f.is_file():
            rel_target.parent.mkdir(exist_ok=True, parents=True)
            copy(str(f.absolute()), str(rel_target))
        if f.is_dir():
            rel_target.mkdir(exist_ok=True)


def has_access(url):
    return current_user.has_role("korrektor") or current_user.has_access(url)


def serve_path(_path, static_folder, title, ignore_access=False):
    try:
        p = safe_join(static_folder, _path)
    except NotFound:
        abort(404)

    if path.basename(_path):
        title = path.basename(_path)

    if path.isdir(p):
        children = []
        c_dirs = []
        for i in listdir(p):
            new_child = {"name": i, "url": url_for(request.endpoint, _path=path.join(_path, i)),
                         "is_dir": path.isdir(path.join(p, i))}
            print(new_child["url"])
            new_child["access"] = ignore_access or new_child["is_dir"] or has_access(new_child["url"])
            if new_child["is_dir"]:
                c_dirs.append(new_child)
            else:
                children.append(new_child)

        children = sorted(c_dirs, key=lambda x: x["name"]) + sorted(children, key=lambda x: x["name"])

        if _path in ["", "/"]:
            parent = url_for("main.index")
        else:
            parent = _path
            if parent.endswith("/"):
                parent = parent[:-1]
            parent = parent.rpartition("/")[0]
            parent = url_for(request.endpoint, _path=parent)
        return render_template("aufgaben_ci/modules.html", title=title, children=children,
                               parent=parent)
    elif path.isfile(p):
        if ignore_access or has_access(url_for(request.endpoint, _path=_path)):
            return send_from_directory(static_folder, _path)
        else:
            abort(403)
    else:
        abort(404)
