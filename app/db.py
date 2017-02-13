from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from app import app

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
