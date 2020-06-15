from flask import Blueprint

app = Blueprint('subject', __name__)

@app.route('/oicjob/api/create_subject',methods=["POST"])
def create_subject():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    db_session.add(Subject(request.json['name']))
    db_session.commit()
    return "true"

@app.route('/oicjob/api/get_subject_all',methods=["POST"])
def get_subject_all():
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    subjects = Subject.query.all()
    return jsonify({'subjects': [subject.to_dict() for subject in subjects]})