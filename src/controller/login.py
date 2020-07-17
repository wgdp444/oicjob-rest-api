from flask import Blueprint, jsonify, request, abort
from models.models import User
from auth.auth import default_auth

app = Blueprint('login', __name__)

@app.route('/oicjob/api/login',methods=["POST"])
def login():
    print(request.json['token'])
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    if User.query.filter(User.google_id==idinfo['sub']).first() is None:
        print('みつからなかったよーゆうてから')
        return jsonify({'result': 'account not found'})
    else:
        print('見つかったよーゆうてから')
        return jsonify({'result': 'account found'})