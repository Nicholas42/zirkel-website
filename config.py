import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Manfs größtes Gehemnis"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GIT_REPO = os.environ.get('REPO_ROOT') or os.path.join(basedir, ".data", "git")
    ORIGIN_URL = os.environ.get('ORIGIN_URL') or "git@github.com:Nicholas42/korrespondenzzirkel.git"

    UPLOADED_SUBMISSIONS_ALLOW = ["tex", "pdf", "tar", "gz", "zip"]
    UPLOADED_REVIEWS_ALLOW = ["txt", "pdf"]
    UPLOADS_DEFAULT_DEST = os.environ.get("UPLOAD_DIR") or os.path.join(basedir, ".data", "submissions")
    UPLOADS_DEFAULT_URL = '/uploads/'

    ADMIN_MAIL = os.environ.get('ADMIN_MAIL') or "root@localhost"
    ADMIN_PW = os.environ.get('ADMIN_PW')

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

