# import flask
from app import application
from app import db
from app import crop
from app import classify_image
from flask import render_template, redirect, url_for, request, session, abort, jsonify, send_file
from sqlalchemy import func, desc, and_, true
import json
import urllib.request
import werkzeug.exceptions as ex
import base64
from tempfile import NamedTemporaryFile

class UnregisteredUser(ex.HTTPException):
    code = 464
    description = '<p>Unregistered User!</p>'


# abort.mappings[464] = UnregisteredUser


@application.route('/')
@application.route('/index')
def index():
    return redirect(url_for('users'))


@application.route('/users/')
def users():
    # users = db.User.query.all()
    return render_template('sql_users.jinja2', users=[])


def parse_token(token):
    auth = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
    data = urllib.request.urlopen(auth+token).read().decode('utf-8')
    return json.loads(data)


def verify(token, email):
    return True
    # data = parse_token(token)
    # if not data['email_verified'] or email != data['email']:
    #     abort(404)


@application.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    token = data['token']
    user = db.User.query.filter_by(email=email).first()
    if user is None:
        # abort(464)
        raise UnregisteredUser
    login = db.Login.query.filter_by(id=user.id).first()
    if login is None:
        verify(token, email)
        db.db.session.add(db.Login(user.id, token))
    elif login.token != token:
        verify(token, email)
        login.token = token
    db.db.session.commit()
    return user.jsonify()


@application.route('/register', methods=['POST'])
def user():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    email = data['email']
    token = data['token']
    photo = data['photo']
    data = parse_token(token)
    verify(data, email)
    user = db.User(username, email, photo)
    try:
        db.db.session.add(user)
        db.db.session.commit()
    except Exception as e:
        abort(400)
    login = db.Login(user.id, token)
    db.db.session.add(login)
    db.db.session.commit()
    return jsonify()


@application.route('/logout', methods=['POST'])
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


@application.route('/popular')
def popular():
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    data = map(lambda x: x.tattoo_id,
               db.db.session.query(db.Likes.tattoo_id, func.count(1))
               .group_by(db.Likes.tattoo_id)
               .order_by(desc(func.count(1)))
               .join(db.Tattoo, db.Tattoo.id == db.Likes.tattoo_id)
               .filter_by(private=False)
               .limit(limit).all())
    data = {i: [tid, db.Tattoo.query.filter_by(id=tid).first().owner_id]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


@application.route('/recent')
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


@application.route('/user-likes')
def liked():
    token = request.args.get('token')
    user_name = request.args.get('user')
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    if user_name == 'null':
        user_id = login.id
    else:
        user_id = db.User.query.filter_by(username=user_name).first().id
    data = db.Likes.query.filter_by(user_id=user_id).join(db.Tattoo, db.Tattoo.id == db.Likes.tattoo_id).filter_by(private=False).limit(limit).all()
    data = {i: [l.tattoo_id, l.owner_id]
            for i, l in enumerate(data)}
    print(data)
    return jsonify(data=data)


# /user-tattoo?private=1
@application.route('/user-tattoo')
def user_tattoo():
    private = request.args.get('private') or '0'
    token = request.args.get('token')
    user_name = request.args.get('user')
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    if user_name == 'null':
        user_id = login.id
    else:
        user_id = db.User.query.filter_by(username=user_name).first().id
    if login.id != user_id and private == '1':
        abort(404)
    data = map(lambda x: (x.id, x.owner_id),
               db.Tattoo.query.filter_by(owner_id=user_id, private=private).limit(limit).all())
    data = {i: [*tid]
            for i, tid in enumerate(data)}
    return jsonify(data=data)


@application.route('/like', methods=['POST'])
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
        abort(400)
    return jsonify()


@application.route('/unlike', methods=['POST'])
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


# @application.route('/following')
# def followed():
#     token = request.args.get('token')
#     searched = request.args.get('searched')
#     user_id = session[token]
#     # if tattoo.owner_id != user_id:
#     #     abort(401)
#     likes = list(db.Follows.query.filter_by(followed_id=searched).map(lambda x: x.jsonify()))
#     return jsonify(likes=likes)


# @application.route('/follower')
# def follower():
#     token = request.args.get('token')
#     searched = request.args.get('searched')
#     user_id = session[token]
#     # if tattoo.owner_id != user_id:
#     #     abort(401)
#     likes = list(db.Follows.query.filter_by(follower_id=searched).map(lambda x: x.jsonify()))
#     return jsonify(likes=likes)


@application.route('/tattoo')
def tattoo():
    tid = request.args.get('id')
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    token = request.args.get('token')
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    path = '../data/'+str(tattoo.id)+'.png'
    return send_file(path)


@application.route('/tattoo-data')
def tattoo_data():
    tid = request.args.get('id')
    token = request.args.get('token')
    user = db.Login.query.filter_by(token=token).first()
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    if user is not None and user.id == tattoo.owner_id:
        data = tattoo.jsonify()
    else:
        data = tattoo.jsonify_other()
    import json
    data = json.loads(data.get_data().decode())
    like = db.Likes.query.filter_by(tattoo_id=tid, user_id=user.id).first()
    data['is_liked'] = False if like is None else True
    return jsonify(**data)


@application.route('/tattoo-update', methods=['POST'])
def tattoo_update():
    data = json.loads(request.get_data(as_text=True))
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
            if t is None:
                t = db.Tag(tag)
                db.db.session.add(t)
                db.db.session.commit()
            ht = db.HasTag(tattoo.id, t.id, tattoo.owner_id)
            db.db.session.add(ht)
        db.db.session.commit()
    return jsonify()


@application.route('/extract-tags', methods=['POST'])
def extract_tags():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    image = data['image']
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    x = data['x']
    y = data['y']
    points = [(px, py) for px, py in zip(x, y) for px, py in zip(px, py)]
    image = base64.b64decode(str.encode(image))
    with NamedTemporaryFile(suffix='.png') as f:
        f.write(image)
        if len(points) > 0:
            crop.crop(f.name, points)
        tags = [tag.split(',')[0] for tag in classify_image.classify(f.name)]
        return jsonify(data=tags)
    return jsonify()


@application.route('/tattoo-upload', methods=['POST'])
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
    db.db.session.add(tattoo)
    db.db.session.commit()
    path = 'data/'+str(tattoo.id) + '.png'
    with open(path, 'wb') as f:
        image = base64.b64decode(str.encode(image))
        f.write(image)
    for tag_desc in data['tags']:
        tag = db.Tag.query.filter_by(desc=tag_desc).first()
        print(tag_desc)
        if tag is None:
            tag = db.Tag(tag_desc)
            db.db.session.add(tag)
            db.db.session.commit()
        tag = db.HasTag(tattoo.id, tag.id, tattoo.owner_id)
        db.db.session.add(tag)
        db.db.session.commit()
    return tattoo.jsonify()


@application.route('/tattoo-delete', methods=['POST'])
def tattoo_delete():
    data = json.loads(request.get_data(as_text=True))
    token = data['token']
    tid = data['email']
    tattoo = db.Tattoo.query.filter_by(id=tid).first()
    login = db.Login.query.filter_by(token=token).first()
    if login is None:
        abort(404)
    user_id = login.id
    if tattoo.owner_id != user_id:
        abort(401)
    db.HasTag.query.filter_by(tattoo_id=tid).delete()
    db.db.session.delete(tattoo)
    db.db.session.commit()
    return jsonify()


@application.route('/search')
def search():
    query = request.args.get('query')
    limit = request.args.get('limit')
    tag = db.Tag.query.filter_by(desc=query).first()
    latest = request.args.get('latest')
    latest = true() if latest is None else db.Tattoo.id < latest
    tags = {i: [x.tattoo_id, x.owner_id] for i, x in
            enumerate(db.HasTag.query
                      .filter_by(tag_id=tag.id)
                      .join(db.Tattoo)
                      .filter_by(private=False)
                      .filter(latest)
                      .order_by(desc(db.Tattoo.id))
                      .limit(limit).all())} if tag is not None else {}
    users = {i: [x.username, x.photo] for i, x in
             enumerate(db.User.query.filter(db.User.username.like('%{}%'.format(query))).
                       limit(limit).all())}
    return jsonify(tags={'data': tags}, users={'data': users})
