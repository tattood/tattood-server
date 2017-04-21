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
    print(token)
    auth = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
    data = urllib.request.urlopen(auth+token).read().decode('utf-8')
    return json.loads(data)


def verify(token, email):
    data = parse_token(token)
    if not data['email_verified'] or email != data['email']:
        abort(404)


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    token = data['token']
    user = db.User.query.filter_by(email=email).first()
    if user is None:
        abort(464)
    login = db.Login.query.filter_by(id=user.id).first()
    if login is None:
        verify(token, email)
        db.db.session.add(db.Login(user.id, token))
    elif login.token != token:
        verify(token, email)
        login.token = token
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
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    data = map(lambda x: x.tattoo_id,
               db.db.session.query(db.Likes.tattoo_id, func.count(1))
               .group_by(db.Likes.tattoo_id).order_by(desc(func.count(1))).limit(limit).all())
    data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


@app.route('/recent')
def recent():
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    data = {i: [x.id, x.owner_id]
            for i, x in
            enumerate(db.Tattoo.query.filter_by(private=False)
                      .order_by(desc(db.Tattoo.uploaded)).limit(limit).all())}
    # data = list(map(lambda x: x.id, db.Tattoo.query.order_by(desc(db.Tattoo.uploaded))
    #                 .limit(20).all()))
    # data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id] for i, tid in enumerate(data)}
    return jsonify(data=data)


@app.route('/user-likes')
def liked():
    token = request.args.get('token')
    user_name = request.args.get('user')
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    print(user_name)
    if user_name == 'null':
        user_id = login.id
    else:
        user_id = db.User.query.filter_by(username=user_name).first().id
    data = db.Likes.query.filter_by(user_id=user_id).limit(limit).all()
    data = {i: [l.tattoo_id, db.Tattoo.query.filter_by(id=l.tattoo_id).first().owner_id]
            for i, l in enumerate(data)}
    return jsonify(data=data)


# /user-tattoo?private=1
@app.route('/user-tattoo')
def user_tattoo():
    private = request.args.get('private') or '0'
    token = request.args.get('token')
    user_name = request.args.get('user')
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    # print("HERE-TOKEN")
    # print(token)
    # user_id = 12
    print(user_name)
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    print(login)
    if user_name == 'null':
        user_id = login.id
    else:
        user_id = db.User.query.filter_by(username=user_name).first().id
    if login.id != user_id and private:
        abort(404)
    data = map(lambda x: (x.id, x.owner_id),
               db.Tattoo.query.filter_by(owner_id=user_id, private=private).limit(limit).all())
    data = {i: [*tid]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


@app.route('/like', methods=['POST'])
def like():
    data = json.loads(request.get_data(as_text=True))
    tid = data['email']
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
        print(e)
        abort(400)
    return jsonify()


@app.route('/unlike', methods=['POST'])
def unlike():
    data = json.loads(request.get_data(as_text=True))
    tid = data['email']
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    db.Likes.query.filter_by(user_id=login.id, tattoo_id=tid).delete()
    db.db.session.commit()
    return jsonify()


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
    login = db.Login.query.filter_by(token=token).first()
    print("TOKEN:"+token)
    if login is None:
        abort(404)
    return send_file('../data/'+str(tattoo.id))


@app.route('/tattoo-data')
def tattoo_data():
    tid = request.args.get('id')
    token = request.args.get('token')
    user = db.Login.query.filter_by(token=token).first()
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    print(tid)
    print(tattoo)
    if user is not None and user.id == tattoo.owner_id:
        data = tattoo.jsonify()
    else:
        data = tattoo.jsonify_other()
    import json
    data = json.loads(data.get_data().decode())
    like = db.Likes.query.filter_by(tattoo_id=tid, user_id=user.id).first()
    data['is_liked'] = 0 if like is None else 1
    print(data)
    return jsonify(**data)


@app.route('/tattoo-update', methods=['POST'])
def tattoo_update():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    tid = data['id']
    private = data['private']
    tags = data['tags']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    tattoo.private = private
    # tattoo.tags = tags
    token = data['token']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
    if tattoo.owner_id != user_id or private is None:
        abort(401)
    db.HasTag.query.filter_by(tattoo_id=tid).delete()
    db.db.session.commit()
    with db.db.session.no_autoflush:
        for tag in tags:
            t = db.Tag.query.filter_by(desc=tag).first()
            print(tag)
            if t is None:
                t = db.Tag(tag)
                db.db.session.add(t)
                db.db.session.commit()
            ht = db.HasTag(tattoo.id, t.id, tattoo.owner_id)
            db.db.session.add(ht)
        db.db.session.commit()
    return jsonify()


@app.route('/tattoo-upload', methods=['POST'])
def tattoo_upload():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    private = True if data['private'] == 'true' else False
    image = data['image']
    if private is None or image is None:
        abort(401)
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    tattoo = db.Tattoo(login.id, private, image)
    import base64
    image = base64.b64decode(str.encode(image))
    db.db.session.add(tattoo)
    db.db.session.commit()
    with open('data/'+str(tattoo.id), 'wb') as f:
        f.write(image)
    tag_c = 0 if data['tag_count'] is None else int(data['tag_count'])
    for i in range(tag_c):
        desc = data['tag{}'.format(i)]
        tag = db.Tag.query.filter_by(desc=desc).first()
        if tag is None:
            tag = db.Tag(desc)
            db.db.session.add(tag)
            db.db.session.commit()
        tag = db.HasTag(tattoo.id, tag.id, tattoo.owner_id)
        db.db.session.add(tag)
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


@app.route('/search')
def search():
    query = request.args.get('query')
    limit = request.args.get('limit')
    print(query)
    tags = {i: [x.tattoo_id, x.owner_id] for i, x in
            enumerate(db.HasTag.query.filter_by(tag_id=query).limit(limit).all())}
    users = {i: [x.id, x.owner_id] for i, x in
             enumerate(db.Tattoo.query.filter(db.User.username.like('%{}%'.format(query))).
                       limit(limit).all())}
    return jsonify(tags={'data': tags}, users={'data': users})
