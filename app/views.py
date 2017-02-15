# import flask
from app import app
from app import db
from flask import render_template, redirect, url_for, request, session, abort, jsonify, send_file
import json
import urllib.request


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('users'))


@app.route('/users/')
def users():
    # users = db.User.query.all()
    return render_template('sql_users.jinja2', users=[])


def parse_token(token):
    auth = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
    data = urllib.request.urlopen(auth+token).read().decode('utf-8')
    return json.loads(data)


def verify(data, email):
    if not data['email_verified'] or email != data['email']:
        abort(404)


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    token = data['token']
    data = parse_token(token)
    verify(data, email)
    user = db.User.query.filter_by(email=data['email']).first()
    if user is None:
        abort(400)
    session[token] = user.username
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
    return redirect(url_for('login'), code=307)


@app.route('/logout', methods=['POST'])
def logout():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    username = session[token]
    if session[token] != username:
        abort(404)
    session.pop(token, None)
    return 200


@app.route('/user-likes')
def liked():
    user_id = 12
    token = request.args.get('token')
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    likes = list(map(lambda x: x.tattoo_id, db.Likes.query.filter_by(user_id=user_id).all()))
    return jsonify(likes=likes)


@app.route('/user-tattoo')
def user_tattoo():
    private = request.args.get('private')
    user_id = 12
    token = request.args.get('token')
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    likes = list(map(lambda x: x.id,
                     db.Tattoo.query.filter_by(owner_id=user_id, private=private).all()))
    return jsonify(likes=likes)


@app.route('/like', methods=['POST'])
def like():
    data = json.loads(request.get_data(as_text=True))
    tid = data['id']
    user_id = 5
    like = db.Likes(user_id, tid)
    token = data['token']
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    try:
        db.db.session.add(like)
        db.db.session.commit()
    except Exception as e:
        abort(400)
    return jsonify('')


@app.route('/unlike', methods=['POST'])
def unlike():
    data = json.loads(request.get_data(as_text=True))
    tid = data['id']
    user_id = 5
    token = data['token']
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    db.Likes.query.filter_by(user_id=user_id, tattoo_id=tid).delete()
    db.db.session.commit()
    return jsonify('')


# @app.route('/user-likes')
# def user_likes():
#     user_id = 12
#     # token = request.args.get('token')
#     # user_id = session[token]
#     # if tattoo.owner_id != user_id:
#     #     abort(401)
#     likes = list(db.Likes.query.filter_by(user_id=user_id).all()
#                  .map(lambda x: x.jsonify()))
#     return jsonify(likes=likes)


# @app.route('/following')
# def followed():
#     token = request.args.get('token')
#     searched = request.args.get('searched')
#     user_id = session[token]
#     # if tattoo.owner_id != user_id:
#     #     abort(401)
#     likes = list(db.Follows.query.filter_by(followed_id=searched).map(lambda x: x.jsonify()))
#     return jsonify(likes=likes)


# @app.route('/follower')
# def follower():
#     token = request.args.get('token')
#     searched = request.args.get('searched')
#     user_id = session[token]
#     # if tattoo.owner_id != user_id:
#     #     abort(401)
#     likes = list(db.Follows.query.filter_by(follower_id=searched).map(lambda x: x.jsonify()))
#     return jsonify(likes=likes)


@app.route('/tattoo')
def tattoo():
    tid = request.args.get('id')
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    token = request.args.get('token')
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    return send_file(tattoo.path, mimetype='image/png')


@app.route('/tattoo-update', methods=['POST'])
def tattoo_update():
    data = json.loads(request.get_data(as_text=True))
    tid = data['id']
    private = data['private']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    tattoo.private = private
    token = data['token']
    user_id = session[token]
    if tattoo.owner_id != user_id or private is None:
        abort(401)
    db.db.session.commit()
    return redirect(url_for('index'))


@app.route('/tattoo-upload', methods=['POST'])
def tattoo_upload():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    username = session[token]
    private = data['private']
    image = request.files['file']
    if private is None or image is None or image.filename == '':
        abort(401)
    tattoo = db.Tattoo(user_id, private, image)
    db.db.session.add(tattoo)
    db.db.session.commit()
    return tattoo.jsonify()


@app.route('/tattoo-delete', methods=['POST'])
def tattoo_delete():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    tid = data['id']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    user_id = session[token]
    if tattoo.owner_id != user_id:
        abort(401)
    tattoo.delete()
    db.db.session.commit()
    return 200
