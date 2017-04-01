import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from app import app
from sqlalchemy.dialects.mysql import TINYTEXT, TEXT


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User {} {}>".format(self.username, self.email)

    def jsonify(self):
        return jsonify(username=self.username, email=self.email)


class Tattoo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, primary_key=True)
    private = db.Column(db.Integer)
    tags = db.Column(db.VARCHAR)
    path = db.Column(TINYTEXT)
    uploaded = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, owner_id, private, data, path):
        self.owner_id = owner_id
        self.private = private
        # [TODO] Should call tag extraction
        self.tags = ""
        # [TODO] Save data and put path
        self.path = path

    def __repr__(self):
        return "<Tatoo {} {}>".format(self.owner_id, self.id)

    def jsonify(self):
        return jsonify(owner_id=self.owner_id, id=self.id, private=self.private)


class Follows(db.Model):
    follower_id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id

    def __repr__(self):
        return "<Follows {} {}>".format(self.follower_id, self.followed_id)

    def jsonify(self):
        return jsonify(follower_id=self.follower_id, followed_id=self.followed_id)


class Likes(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    tattoo_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, tattoo_id):
        self.user_id = user_id
        self.tattoo_id = tattoo_id

    def __repr__(self):
        return "<Likes {} {}>".format(self.user_id, self.tattoo_id)

    def jsonify(self):
        return jsonify(user_id=self.user_id, tattoo_id=self.tattoo_id)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(20))

    def __init__(self, desc):
        self.desc = desc

    def __repr__(self):
        return "<Tag {} {}>".format(self.id, self.desc)

    def jsonify(self):
        return jsonify(desc=self.desc)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(TEXT)

    def __init__(self, _id, token):
        self.id = _id
        self.token = token

    def jsonify(self):
        return jsonify(id=self.id, token=self.token)
