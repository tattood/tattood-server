# import flask
from app import app
from app import db
from flask import render_template, redirect, url_for, request, session, abort, jsonify, send_file
from sqlalchemy import func, desc
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
    user = db.User.query.filter_by(email=email).first()
    if user is None:
        abort(400)
    login = db.Login.query.filter_by(id=user.id).first()
    # print(login)
    if login is None:
        db.db.session.add(db.Login(user.id, token))
        db.db.session.commit()
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
    login = db.Login(user.id, token)
    db.db.session.add(login)
    db.db.session.commit()
    return jsonify()


@app.route('/logout', methods=['POST'])
def logout():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    else:
        db.db.session.delete(login)
        db.db.session.commit()
    return jsonify()


@app.route('/popular')
def popular():
    limit = int(request.args.get('limit'))
    data = map(lambda x: x.tattoo_id,
               db.db.session.query(db.Likes.tattoo_id, func.count(1))
               .group_by(db.Likes.tattoo_id).order_by(desc(func.count(1))).limit(limit).all())
    data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


@app.route('/recent')
def recent():
    limit = int(request.args.get('limit'))
    data = {i: [x.id, x.owner_id]
            for i, x in
            enumerate(db.Tattoo.query.order_by(desc(db.Tattoo.uploaded)).limit(limit).all())}
    # data = list(map(lambda x: x.id, db.Tattoo.query.order_by(desc(db.Tattoo.uploaded))
    #                 .limit(20).all()))
    # data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id] for i, tid in enumerate(data)}
    return jsonify(data=data)


@app.route('/user-likes')
def liked():
    token = request.args.get('token')
    user_id = 12
    # login = db.Login.query.filter_by(token=token).first()
    # if login is None:
    #     abort(404)
    # user_id = login.id
    data = map(lambda x: x.tattoo_id,
               db.db.session.query(db.Likes.tattoo_id, func.count(1))
               .filter_by(user_id=user_id)
               .group_by(db.Likes.tattoo_id).order_by(desc(func.count(1))).limit(20).all())
    data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


# /user-tattoo?private=1
@app.route('/user-tattoo')
def user_tattoo():
    private = request.args.get('private') or '0'
    token = request.args.get('token')
    # print("HERE-TOKEN")
    # print(token)
    user_id = 12
    # login = db.Login.query.filter_by(token=token).first()
    # print(login)
    # if login is None:
    #     abort(404)
    # user_id = login.id
    data = map(lambda x: x.id,
               db.db.session.query(db.Tattoo.id, db.Tattoo.owner_id, func.count(1))
               .filter_by(owner_id=user_id, private=private)
               .group_by(db.Tattoo.id).order_by(desc(func.count(1))).limit(20).all())
    data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id]
            for i, tid in enumerate(data)}
    # print("HERE")
    # print(data)
    return jsonify(data=data)


@app.route('/like', methods=['POST'])
def like():
    data = json.loads(request.get_data(as_text=True))
    tid = data['id']
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
    like = db.Likes(user_id, tid)
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
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
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
    # login = db.Login.query.filter_by(token=token).first()
    # print("TOKEN:"+token)
    # if login is None:
    #     abort(404)
    # user_id = login.id
    # if tattoo.private and tattoo.user_id != user_id:
    #     abort(404)
    return send_file('../data/'+tattoo.path, mimetype='image/png')


@app.route('/tattoo-data')
def tattoo_data():
    tid = request.args.get('id')
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    print(tattoo.jsonify_other().data)
    return tattoo.jsonify_other()


@app.route('/tattoo-update', methods=['POST'])
def tattoo_update():
    data = json.loads(request.get_data(as_text=True))
    tid = data['id']
    private = data['private']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    tattoo.private = private
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
    if tattoo.owner_id != user_id or private is None:
        abort(401)
    db.db.session.commit()
    return redirect(url_for('index'))


@app.route('/tattoo-upload', methods=['POST'])
def tattoo_upload():
    data = request.form
    token = data['token']
    private = True if data['private'] == 'true' else False
    image = data['image']
    name = data['name']
    if private is None or image is None or name == '':
        abort(401)
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    tattoo = db.Tattoo(login.id, private, image, name)
    import base64
    image = base64.b64decode(str.encode(image))
    print(image)
    with open('data/'+name, 'wb') as f:
        f.write(image)
    db.db.session.add(tattoo)
    db.db.session.commit()
    return tattoo.jsonify()


@app.route('/tattoo-delete', methods=['POST'])
def tattoo_delete():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    tid = data['id']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
    if tattoo.owner_id != user_id:
        abort(401)
    tattoo.delete()
    db.db.session.commit()
    return 200
