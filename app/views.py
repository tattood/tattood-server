# import flask
from app import app
from app import db
from flask import render_template, redirect, url_for, request, jsonify


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
    if request.method == 'GET':
        username = request.args.get('username')
        # email = request.args.get('email')
        user = db.User.query.filter_by(username=username).first()
        if user is None:
            return jsonify()
        return jsonify(username=user.username, email=user.email)
    elif request.method == 'POST':
        new_user = db.User(request.form['username'], request.form['email'])
        db.db.session.add(new_user)
        db.db.session.commit()
    return redirect(url_for('index'))
