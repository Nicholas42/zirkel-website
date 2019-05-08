from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"


def build_app(conf: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.aufgaben_ci import bp as ci_bp
    app.register_blueprint(ci_bp, url_prefix="/ci")
    app.view_functions["aufgaben_ci.static"] = login_required(ci_bp.send_static_file)
    print(app.view_functions)

    return app
