from flask import Blueprint, jsonify, request, abort, make_response
from models.models import Industry
from auth.auth import default_auth
from database import db
from sqlalchemy.exc import IntegrityError
from controller.modules import common
import traceback
from datetime import datetime
from flask_jwt_extended import jwt_required

app = Blueprint('industry', __name__)

@app.route('/oicjob/api/industry/create',methods=["POST"])
def create_industry():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        db.session.add(Industry(request.json['name']))
        db.session.commit()
        return jsonify({'result': True}), 201
    except:
        return jsonify({'result': False}), 500
    
@app.route('/oicjob/api/industry/gets',methods=["POST"])
def get_industry_all():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    industrys = Industry.query.all()
    return jsonify({'industrys': [industry.to_dict() for industry in industrys]})

@app.route('/oicjob/api/industry/get/<int:id>',methods=["POST"])
def get_industry(id):
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    industry = Industry.query.filter_by(id=id).first()
    return jsonify(industry.to_dict())

@app.route('/oicjob/api/industry/update/<int:id>',methods=["POST"])
def update_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        industry = Industry.query.filter_by(id=id).first()
        if industry is None:
            return jsonify({'message': 'record not found'}), 400
        industry.name = request.json['name']
        industry.updated_by = request.json['updated_by']
        industry.updated = datetime.now()
        db.session.commit()
        return make_response('', 204)
    except Exception as e:
        return jsonify({'message': 'failed'}), 500

@app.route('/oicjob/api/industry/delete/<int:id>',methods=["POST"])
def delete_industry(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])   
    if idinfo is None:
        abort(403)
    try:
        industry = Industry.query.filter_by(id=id).first()
        if industry is None:
            return jsonify({'message': 'record not found'}), 400
        db.session.delete(industry)
        db.session.commit()
        return make_response('', 204)
    except:
        # print(traceback.format_exc())
        return jsonify({'message': 'failed'}), 500

@app.route('/oicjob/api/industry/seartches',methods=["POST"])
def searches_industry():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    searches_request = {}
    # カラムを取得して検索条件に指定されているかをチェックする
    # NOTE: モデル名.__table__.c.keys()でカラムの一覧を取得できる
    for column in Industry.__table__.c.keys():
        if column in request.json.keys():
            searches_request[column] = request.json[column]
        else:
            searches_request[column] = None

    industrys = common.search_query(Industry, searches_request)
    return jsonify({'industrys': [industry.to_dict() for industry in industrys]})