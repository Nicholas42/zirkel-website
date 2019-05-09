from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
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
    active = db.Column(db.Boolean)

    roles = db.relationship("Role", secondary=user_roles)
    reviews = db.relationship("Review", back_populates="reviewer")
    submissions = db.relationship("Submission", back_populates="author")

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

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

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="submissions")

    upload_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.String)
    filename = db.Column(db.String)
    fileurl = db.Column(db.String)

    review = db.relationship("Review", back_populates="submission", uselist=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    submission_id = db.Column(db.Integer, db.ForeignKey("submission.id"), unique=True)
    submission = db.relationship("Submission", back_populates="review")

    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    reviewer = db.relationship("User", back_populates="reviews")

    notes = db.Column(db.String)
    filename = db.Column(db.String)
    fileurl = db.Column(db.String)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
