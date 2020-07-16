from flask import Blueprint, jsonify, request, abort
from models.models import JobOffer
from auth.auth import default_auth
from database import db
from sqlalchemy.exc import IntegrityError

app = Blueprint('joboffer', __name__)

@app.route('/oicjob/api/get_joboffer/all',methods=["POST"])
def get_joboffer_all():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    joboffer = JobOffer.query.all()
    return jsonify({'joboffers':[joboffer.to_dict() for joboffer in joboffer]})

@app.route('/oicjob/api/create_joboffer',methods=["POST"])
def create_joboffer():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        db.session.add(JobOffer(request.json['industry_id'],request.json['occupation'],
                                request.json['max_appicants'],request.json['starting_salary'],
                                request.json['image_url_text']))
        db.session.commit()
        return jsonify({'result': True})
    except IntegrityError as e:
        # スタックトレース
        print(traceback.format_exc())
        return jsonify({'result': False})

@app.route('/oicjob/api/delete_joboffer',methods=["POST"])
def delete_joboffer():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        jobinfo = JobOffer.query.filter_by(id=request.json['id']).first()
        db.session.delete(jobinfo)
        db.session.commit()
        return jsonify({'result': True})
    except:
        return jsonify({'result': False})

@app.route('/oicjob/api/update_joboffer',methods=["POST"])
def update_joboffer():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    try:
        jobinfo = JobOffer.query.filter(id=request.json['id']).first()
        jobinfo.industry_id = request.json['industry_id']
        jobinfo.occupation = request.json['occupation'] 
        jobinfo.max_appicants = request.json['max_appicants']
        jobinfo.starting_salary = request.json['starting_salary']
        jobinfo.image_url_text = request.json['image_url_text']
        jobinfo.updated = request.json['updated']
        jobinfo.updated_by = request.json['updated_by']
        db.session.commit()
        return jsonify({'result': True})
    except:
        return jsonify({'result': False})