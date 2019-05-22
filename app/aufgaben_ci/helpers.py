import os
from os import path, listdir

from flask import safe_join, render_template, send_from_directory, abort
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from shutil import copy
from subprocess import run, DEVNULL
from pathlib import Path

from werkzeug.exceptions import NotFound

LATEXMK_CALL = ["latexmk", "-cd", "-norc", "-pdf", "-quiet"]
ALL_PATTERN = "**/*"
PDF_PATTERN = "**/*.pdf"


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
        ret = run(LATEXMK_CALL + [str(f.absolute())], env=env, stdout=DEVNULL, stderr=DEVNULL, cwd=str(f.parent.absolute()))
        if ret.returncode != 0:
            errors.append(str(f.relative_to(directory)))

    return runs, errors


def copy_rec(source, target, allowed=ALL_PATTERN):
    source = Path(source)
    target = Path(target)
    for f in source.glob(allowed):
        rel_target = target.joinpath(f.relative_to(source))
        if f.is_file():
            rel_target.parent.mkdir(exist_ok=True, parents=True)
            copy(str(f.absolute()), str(rel_target))
        if f.is_dir():
            rel_target.mkdir(exist_ok=True)


def serve_path(_path, static_folder):
    try:
        p = safe_join(static_folder, _path)
    except NotFound:
        abort(404)

    if path.isdir(p):
        children = []
        for i in listdir(p):
            children.append({"name": i, "path": path.join(_path, i)})
        return render_template("aufgaben_ci/modules.html", title=path.basename(p), children=children)
    elif path.isfile(p):
        return send_from_directory(static_folder, _path)
    else:
        abort(404)
