from datetime import datetime,timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from .extensions import db


class User(UserMixin,db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    
    urls = db.relationship(
        "URL",
        backref="owner",
        lazy=True,
        cascade="all,delete-orphan"
    )
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class URL(db.Model):
    
    __tablename__ = "urls"
    
    id = db.Column(db.Integer,primary_key=True)
    original_url = db.Column(db.Text,nullable=False)
    short_code = db.Column(db.String(20),unique=True,nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )
    
    clicks = db.relationship(
        "Click",
        backref = "url",
        lazy = True,
        cascade = "all,delete-orphan"
    )


class Click(db.Model):
    __tablename__ = "clicks"
    
    id = db.Column(db.Integer,primary_key=True)
    clicked_at = db.Column(
        db.DateTime,
        default=lambda:datetime.now(timezone.utc),
        nullable=False
    )
    
    url_id = db.Column(
        db.Integer,
        db.ForeignKey("urls.id"),
        nullable = False
    )