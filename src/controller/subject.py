from flask import Blueprint, jsonify, request, abort
from models.models import Subject
from auth.auth import default_auth
from database import db
from controller.modules import common

import traceback

from datetime import datetime

app = Blueprint('subject', __name__)

@app.route('/oicjob/api/create_subject',methods=["POST"])
def create_subject():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        db.session.add(Subject(request.json['name']))
        db.session.commit()
        return jsonify({'result': True}), 201
    except:
        return jsonify({'result': False})
    

@app.route('/oicjob/api/subject/get',methods=["POST"])
def get_subject_all():
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    subjects = Subject.query.all()
    return jsonify({'subjects': [subject.to_dict() for subject in subjects]})

@app.route('/oicjob/api/subject/update/<int:id>',methods=["POST"])
def update_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        subject = Subject.query.filter_by(id=id).first()
        if subject is None:
            return jsonify({'result': 'record not found'}), 400
        subject.name = request.json['name']
        subject.updated_by = request.json['updated_by']
        subject.updated = datetime.now()
        db.session.commit()
        return jsonify({'result': True}), 204
    except Exception as e:
        return jsonify({'result': False}), 500

@app.route('/oicjob/api/subject/delete/<int:id>',methods=["POST"])
def delete_subject(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        subject = Subject.query.filter_by(id=id).first()
        if subject is None:
            return jsonify({'result': 'record not found'}), 400
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'result': True}), 204
    except:
        # print(traceback.format_exc())
        return jsonify({'result': False}), 500

@app.route('/oicjob/api/subject/seartches',methods=["POST"])
def searches_subject():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    searches_request = {}
    # カラムを取得して検索条件に指定されているかをチェックする
    # NOTE: モデル名.__table__.c.keys()でカラムの一覧を取得できる
    for column in Subject.__table__.c.keys():
        if column in request.json.keys():
            searches_request[column] = request.json[column]
        else:
            searches_request[column] = None

    subjects = common.search_query(Subject, searches_request)
    return jsonify({'subjects': [subject.to_dict() for subject in subjects]})
        