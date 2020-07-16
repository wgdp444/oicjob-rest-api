from flask import Blueprint, jsonify, request, abort, make_response
from models.models import Subject
from auth.auth import default_auth
from database import db
from controller.modules import common
import json

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
        return jsonify({'result': False}), 500
    

@app.route('/oicjob/api/subject/get',methods=["POST"])
def get_subject_all():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    subjects = Subject.query.all()
    return jsonify({'subjects': [subject.to_dict() for subject in subjects]})

@app.route('/oicjob/api/subject/get/<int:id>',methods=["POST"])
def get_subject(id):
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    subject = Subject.query.filter_by(id=id).first()
    return jsonify(subject.to_dict())

@app.route('/oicjob/api/subject/update/<int:id>',methods=["POST"])
def update_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        subject = Subject.query.filter_by(id=id).first()
        if subject is None:
            return jsonify({'message': 'record not found'}), 400
        subject.name = request.json['name']
        subject.updated_by = request.json['updated_by']
        subject.updated = datetime.now()
        db.session.commit()
        return make_response('', 204)
    except Exception as e:
        return jsonify({'message': 'failed'}), 500

@app.route('/oicjob/api/subject/delete/<int:subject_id>',methods=["POST"])
def delete_subject(subject_id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])   
    if idinfo is None:
        abort(403)
    try:
        subject = Subject.query.filter_by(id=subject_id).first()
        if subject is None:
            return jsonify({'message': 'record not found'}), 400
        db.session.delete(subject)
        db.session.commit()
        return make_response('', 204)
    except:
        # print(traceback.format_exc())
        return jsonify({'message': 'failed'}), 500

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
        