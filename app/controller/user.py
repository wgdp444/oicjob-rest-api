from flask import Blueprint

app = Blueprint('user', __name__)

@app.route('/oicjob/api/create_user',methods=["POST"])
def create_user():
    idinfo = default_auth(request.headers['Content-Type'])
    if idinfo is None:
        abort(403)
    try:
        db_session.add(User(idinfo['sub'], request.json['subject_id'], request.json['is_admin'], class_number=request.json['class_number']))
        db_session.commit()
        return "true"
    except IntegrityError as e:
        # print(traceback.format_exc())
        return "false"

@app.route('/oicjob/api/get_user',methods=["POST"])
def get_user():
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    user = User.query.filter(User.google_id==idinfo['sub'])
    print(user)