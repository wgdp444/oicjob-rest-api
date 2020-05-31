from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from auth.auth import default_auth
from models.models import User, Subject
from models.database import db_session

from sqlalchemy.exc import IntegrityError

import traceback

app = Flask(__name__)
CORS(app)
@app.errorhandler(403)
def forbidden(e):
    return jsonify({'result': 'forbidden'})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'result': 'not found'})

@app.errorhandler(Exception)
def api_error(e):
    return jsonify({'result': 'api error'}), 500

@app.route('/oicjob/api/login',methods=["POST"])
def login():
    print(request.json['token'])
    idinfo = default_auth(request.json['token'], request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    if User.query.filter(User.id==idinfo['sub']).first() is None:
        print('みつからなかったよーゆうてから')
        return jsonify({'result': 'account not found'})
    else:
        print('見つかったよーゆうてから')
        return jsonify({'result': 'account found'})

@app.route('/oicjob/api/get_user',methods=["POST"])
def get_user():
    idinfo = default_auth(request.json['token'], request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    user = User.query.filter(User.id==idinfo['sub'])
    print(user)

@app.route('/oicjob/api/get_subject_all',methods=["POST"])
def get_subject_all():
    idinfo = default_auth(request.json['token'], request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    subjects = Subject.query.all()
    return jsonify({'subjects': [subject.to_dict() for subject in subjects]})

@app.route('/oicjob/api/create_user',methods=["POST"])
def create_user():
    idinfo = default_auth(request.json['token'], request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    try:
        db_session.add(User(request.json['id'], request.json['subject_id'], request.json['is_admin'], class_number=request.json['class_number']))
        db_session.commit()
        return "true"
    except IntegrityError as e:
        # print(traceback.format_exc())
        return "false"
        

@app.route('/oicjob/api/create_subject',methods=["POST"])
def create_subject():
    idinfo = default_auth(request.json['token'], request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    db_session.add(Subject(request.json['name']))
    db_session.commit()
    return "true"

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=4649)