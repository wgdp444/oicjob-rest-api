from flask import Blueprint, jsonify, request, abort, make_response
from models.models import JobOffer
from auth.auth import default_auth
from database import db
from sqlalchemy.exc import IntegrityError
from controller.modules import common
import traceback
from datetime import datetime
from flask_jwt_extended import jwt_required

app = Blueprint('joboffer', __name__)

@app.route('/oicjob/api/joboffer/gets',methods=["POST"])
@jwt_required
def get_joboffer_all():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    joboffers = JobOffer.query.all()
    print(request.headers)
    return jsonify({'joboffers': [joboffer.to_dict() for joboffer in joboffers]})

@app.route('/oicjob/api/joboffer/get/<int:id>',methods=["POST"])
@jwt_required
def get_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    joboffer = JobOffer.query.filter_by(id=id).first()
    return jsonify(joboffer.to_dict())


@app.route('/oicjob/api/joboffer/create',methods=["POST"])
@jwt_required
def create_joboffer():
    # idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    # if idinfo is None:
    #     abort(403)
    try:
        db.session.add(JobOffer(request.json['company_name'], request.json['industry_id'], 
                                request.json['occupation'], request.json['max_appicants'],
                                request.json['starting_salary'], request.json['image_url_text']))
        db.session.commit()
        return jsonify({'result': True}), 201
    except IntegrityError as e:
        # スタックトレース
        print(traceback.format_exc())
        return jsonify({'result': False}), 500

@app.route('/oicjob/api/joboffer/delete/<int:id>',methods=["POST"])
def delete_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        jobinfo = JobOffer.query.filter_by(id=id).first()
        db.session.delete(jobinfo)
        db.session.commit()
        return make_response('', 204)
    except:
        print(traceback.format_exc())
        return jsonify({'result': False}), 500

@app.route('/oicjob/api/joboffer/update/<int:id>',methods=["POST"])
def update_joboffer(id):
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        jobinfo = JobOffer.query.filter_by(id=id).first()
        jobinfo.company_name = request.json['company_name']
        jobinfo.industry_id = request.json['industry_id']
        jobinfo.occupation = request.json['occupation'] 
        jobinfo.max_appicants = request.json['max_appicants']
        jobinfo.starting_salary = request.json['starting_salary']
        jobinfo.image_url_text = request.json['image_url_text']
        jobinfo.updated = datetime.now()
        jobinfo.updated_by = request.json['updated_by']
        db.session.commit()
        return make_response('', 204)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'result': False}), 500

@app.route('/oicjob/api/joboffer/seartches',methods=["POST"])
def searches_joboffer():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    searches_request = {}
    # カラムを取得して検索条件に指定されているかをチェックする
    # NOTE: モデル名.__table__.c.keys()でカラムの一覧を取得できる
    for column in JobOffer.__table__.c.keys():
        if column in request.json.keys():
            searches_request[column] = request.json[column]
        else:
            searches_request[column] = None

    joboffers = common.search_query(JobOffer, searches_request)
    return jsonify({'joboffers': [joboffer.to_dict() for joboffer in joboffers]})