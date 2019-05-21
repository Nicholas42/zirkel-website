from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import string
import secrets

PW_ALPHABET = string.ascii_letters + string.digits

from app import db, login

user_roles = db.Table(
    "user_roles",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)

    roles = db.relationship("Role", secondary=user_roles)

    def __init__(self, username, email, roles=[], active=True):
        self.username = username
        self.email = email
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


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    reviewer = db.relationship("User", foreign_keys=[reviewer_id])

    notes = db.Column(db.String)
    filename = db.Column(db.String)
    fileurl = db.Column(db.String)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
