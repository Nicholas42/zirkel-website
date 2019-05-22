from flask.cli import with_appcontext

from app import db
import click
from app.models import Role, User, user_roles
from app.aufgaben_ci.routes import pullhook


def register(app):
    @app.cli.group()
    def init_git():
        """ Initialize the git repo for modules. """
        pass

    @init_git.command()
    def run():
        with app.app_context():
            pullhook()

    @app.cli.group()
    def init_db():
        """ Initialize the database with important static data."""
        pass

    def add_role(r):
        if Role.query.filter_by(name=r).first() is None:
            db.session.add(Role(name=r))

    @init_db.command()
    def roles():
        """ Adds important userroles. """
        for r in ["admin", "korrektor"]:
            add_role(r)

        db.session.commit()

    @init_db.command()
    @click.option('--password', default=app.config["ADMIN_PW"])
    def add_admin(password):
        """ Adds the admin with the given password. Changes password if there is already one. """
        if password is None:
            raise RuntimeError("Password may not be None.")
        add_role("admin")

        admin = User.query.filter_by(username="admin").first()

        if admin is None:
            admin = User(username="admin", email=app.config["ADMIN_MAIL"], active=True)
            db.session.add(admin)

        admin.set_password(password)
        admin.roles.append(Role.query.filter_by(name="admin").first())

        db.session.commit()
