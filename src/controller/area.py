from flask import Blueprint, jsonify, request, abort, make_response
from models.models import Area
from auth.auth import default_auth
from database import db
from sqlalchemy.exc import IntegrityError
from controller.modules import common
import traceback
from datetime import datetime
from flask_jwt_extended import jwt_required

app = Blueprint('area', __name__)

@app.route('/oicjob/api/area/create',methods=["POST"])
def create_area():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        db.session.add(Area(request.json['prefecture'], request.json['job_offer_id']))
        db.session.commit()
        return jsonify({'result': True}), 201
    except:
        return jsonify({'result': False}), 500
    
@app.route('/oicjob/api/area/gets',methods=["POST"])
def get_area_all():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    areas = Area.query.all()
    return jsonify({'areas': [area.to_dict() for area in areas]})

@app.route('/oicjob/api/area/get/<int:id>',methods=["POST"])
def get_area(id):
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    area = Area.query.filter_by(id=id).first()
    return jsonify(area.to_dict())

@app.route('/oicjob/api/area/update/<int:id>',methods=["POST"])
def update_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        area = Area.query.filter_by(id=id).first()
        if area is None:
            return jsonify({'message': 'record not found'}), 400
        area.prefecture = request.json['prefecture']
        area.job_offer_id = request.json['job_offer_id']
        # area.updated_by = request.json['updated_by']
        area.updated = datetime.now()
        db.session.commit()
        return make_response('', 204)
    except Exception as e:
        return jsonify({'message': 'failed'}), 500

@app.route('/oicjob/api/area/delete/<int:id>',methods=["POST"])
def delete_area(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])   
    if idinfo is None:
        abort(403)
    try:
        area = Area.query.filter_by(id=id).first()
        if area is None:
            return jsonify({'message': 'record not found'}), 400
        db.session.delete(area)
        db.session.commit()
        return make_response('', 204)
    except:
        # print(traceback.format_exc())
        return jsonify({'message': 'failed'}), 500

@app.route('/oicjob/api/area/seartches',methods=["POST"])
def searches_area():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    searches_request = {}
    # カラムを取得して検索条件に指定されているかをチェックする
    # NOTE: モデル名.__table__.c.keys()でカラムの一覧を取得できる
    for column in Area.__table__.c.keys():
        if column in request.json.keys():
            searches_request[column] = request.json[column]
        else:
            searches_request[column] = None

    areas = common.search_query(Area, searches_request)
    return jsonify({'areas': [area.to_dict() for area in areas]})