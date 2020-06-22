from flask import Blueprint, jsonify, request, abort
from models.models import JobOffer
from auth.auth import default_auth
from database import db

app = Blueprint('joboffer', __name__)

@app.route('/oicjob/api/get_joboffer/all',methods=["POST"])
def get_joboffer_all():
    # idinfo = default_auth(request.headers['Content-Type'])
    # if idinfo is None:
    #     abort(403)
    joboffer = JobOffer.query.all()
    return jsonify({'joboffer':[joboffer.to_dict() for joboffer in joboffer]})

@app.route('/oicjob/api/create_joboffer',methods=["POST"])
def create_joboffer():
    # idinfo = default_auth(request.headers['Content-Type'])
    # if idinfo is None:
    #     abort(403)
    try:
        db.session.add(JobOffer(request.json['industry_id'],request.json['occupation'],
                                request.json['max_appicants'],request.json['starting_salary'],
                                request.json['image_url_text']))
        db.session.comit()
        return "true"
    except IntegrityError as e:
        # print(traceback.format_exc())
        return "false"
    