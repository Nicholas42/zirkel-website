from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from flask_uploads import UploadSet, configure_uploads
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
submissions = UploadSet("submissions")


def build_app(conf: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    configure_uploads(app, submissions)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.aufgaben_ci import bp as ci_bp
    app.register_blueprint(ci_bp, url_prefix="/ci")
    app.view_functions["aufgaben_ci.static"] = login_required(ci_bp.send_static_file)

    from app.upload import bp as upload_bp
    app.register_blueprint(upload_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
