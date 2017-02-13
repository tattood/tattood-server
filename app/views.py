# import flask
from app import app
from app import db
from flask import render_template, redirect, url_for, request, jsonify, abort
import json


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('users'))


@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        return redirect(url_for('user'), code=307)
    users = db.User.query.all()
    return render_template('sql_users.jinja2', users=users)


@app.route('/user', methods=['GET', 'POST'])
def user():
    user = None
    if request.method == 'GET':
        # username = request.args.get('username')
        email = request.args.get('email')
        user = db.User.query.filter_by(email=email).first()
    elif request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        username = data['username']
        email = data['email']
        if not username or not email:
            abort(404)
        user = db.User(username, email)
        try:
            db.db.session.add(user)
            db.db.session.commit()
        except Exception as e:
            abort(400)
    if user is not None:
        return jsonify(username=user.username, email=user.email)
    else:
        abort(404)
