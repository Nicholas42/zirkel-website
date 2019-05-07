from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def build_app(conf: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
