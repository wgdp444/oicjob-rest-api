from flask import Blueprint, jsonify, request, abort
from models.models import User
from auth.auth import default_auth
from database import db

from sqlalchemy.exc import IntegrityError

app = Blueprint('user', __name__)

@app.route('/oicjob/api/create_user',methods=["POST"])
def create_user():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        db.session.add(User(idinfo['sub'], request.json['subject_id'], request.json['is_admin'], class_number=request.json['class_number']))
        db.session.commit()
        return jsonify({'result': True})
    except IntegrityError as e:
        # print(traceback.format_exc())
        return hsonify({'result': False})

@app.route('/oicjob/api/get_user',methods=["POST"])
def get_user():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    user = User.query.filter(User.google_id==idinfo['sub']).first()
    return jsonify(user.to_dict())