from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login

user_roles = db.Table(
    "user_roles",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship("Role", secondary=user_roles)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
