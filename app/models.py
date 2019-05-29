import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import string
import secrets
from app import db, login

PW_ALPHABET = string.ascii_letters + string.digits

user_roles = db.Table(
    "user_roles",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

modules_per_user = db.Table(
    "modules_per_user",
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, unique=True)

    permitted_users = db.relationship("User", secondary=modules_per_user)

    def is_permitted(self, user):
        return user.has_role("korrektor") or user in self.permitted_users


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)

    next_module = db.Column(db.Date)
    next_sub = db.Column(db.Date)
    next_subject = db.Column(db.String)

    roles = db.relationship("Role", secondary=user_roles)
    unlocked_modules = db.relationship("Module", secondary=modules_per_user)

    def __init__(self, username, email, roles=None, active=True):
        self.username = username
        self.email = email
        if self.roles is None:
            self.roles = []
        else:
            self.roles = roles
        self.active = active

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def set_random_password(self):
        pw = ''.join(secrets.choice(PW_ALPHABET) for i in range(12))
        self.set_password(pw)
        return pw

    def has_role(self, role_name: str):
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            raise RuntimeError("Role %s does not exist." % role_name)
        return role in self.roles

    def is_admin(self):
        return self.has_role("admin")

    @property
    def is_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def get_reset_password_token(self, expires_in=timedelta(seconds=600)):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.now() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def has_access(self, p):
        mod = Module.query.filter_by(path=p).first()
        return mod is not None and mod in self.unlocked_modules

    def get_next_module(self, alt=""):
        if self.next_module:
            return self.next_module.strftime("%d.%m.%Y")
        else:
            return alt

    def get_next_sub(self, alt=""):
        if self.next_sub:
            return self.next_sub.strftime("%d.%m.%Y")
        else:
            return alt


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    upload_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.String)
    filename = db.Column(db.String)
    fileurl = db.Column(db.String)

    # Foreign Keys
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"))

    # Relationships
    reviewer = db.relationship("User", foreign_keys=[reviewer_id])
    author = db.relationship("User", foreign_keys=[author_id])
    review = db.relationship("Review", foreign_keys=[review_id], backref=backref("submission", uselist=False))

    def is_open(self):
        return self.review is None

    def is_claimed(self):
        return self.reviewer is not None

    def status(self):
        if self.is_open() and not self.is_claimed():
            return "offen"
        elif self.is_open() and self.is_claimed():
            return "wird korrigiert"
        else:
            return "korrigiert"

    def get_upload_time(self):
        return self.upload_time.strftime("%d.%m.%Y %H:%M")

    def get_upload_date(self):
        return self.upload_time.strftime("%d.%m.%Y")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    reviewer = db.relationship("User", foreign_keys=[reviewer_id])

    points = db.Column(db.Float)
    notes = db.Column(db.String)
    filename = db.Column(db.String)
    fileurl = db.Column(db.String)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
