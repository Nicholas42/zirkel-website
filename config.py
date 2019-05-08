import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = "Manfs größtes Gehemnis"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GIT_REPO = os.environ.get('REPO_ROOT') or os.path.join(basedir, "app", ".data", "git")
    ORIGIN_URL = os.environ.get('ORIGIN_URL') or "git@github.com:Nicholas42/korrespondenzzirkel.git"
