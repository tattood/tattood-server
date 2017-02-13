# import flask
from app import app
from app import db
from flask import render_template, redirect, url_for, request, jsonify, abort
import json
import urllib.request


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('users'))


@app.route('/users/')
def users():
    users = db.User.query.all()
    return render_template('sql_users.jinja2', users=users)


def parse_token(token):
    auth = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
    data = urllib.request.urlopen(auth+token).read().decode('utf-8')
    return json.loads(data)


def verify(data, email):
    if not data['email_verified'] or email != data['email']:
        abort(404)


@app.route('/login', methods=['POST'])
def login():
    email = request.args.get('email')
    token = request.args.get('token')
    data = parse_token(token)
    verify(data, email)
    user = db.User.query.filter(email=data['email']).first()
    return user.jsonify()


@app.route('/register', methods=['POST'])
def user():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    email = data['email']
    token = data['token']
    data = parse_token(token)
    verify(data, email)
    user = db.User(username, email)
    try:
        db.db.session.add(user)
        db.db.session.commit()
    except Exception as e:
        abort(400)
    return user.jsonify()
