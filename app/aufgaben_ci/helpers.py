from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from shutil import copy
from subprocess import run, DEVNULL
from pathlib import Path

LATEXMK_CALL = ["latexmk", "-cd", "-norc", "-pdf", "-quiet"]
ALL_PATTERN = "**/*"
PDF_PATTERN = "**/*.pdf"


def pull_repo(git_path, upstream_url):
    try:
        repo = Repo(git_path)
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.clone_from(upstream_url, git_path)

    repo.git.pull()


def make_all(directory):
    directory = Path(directory)
    runs = 0
    errors = []
    for f in directory.glob("**/*.tex"):
        runs += 1
        ret = run(LATEXMK_CALL + [str(f.absolute())], stdout=DEVNULL, stderr=DEVNULL)
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
