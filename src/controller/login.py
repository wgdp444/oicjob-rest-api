from flask import Blueprint, jsonify, request, abort, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token, jwt_refresh_token_required


from models.models import User
from auth.auth import default_auth

app = Blueprint('login', __name__)

@app.route('/oicjob/api/login',methods=["POST"])
def login():
    print(request.json['token'])
    idinfo = default_auth(request.headers['Content-Type'], request.json['token'])
    if idinfo is None:
        abort(403)
    if User.query.filter_by(google_id=idinfo['sub']).first() is None:
        return make_response('', 204)
    
    print('見つかったよーゆうてから')
    return jsonify({
        'access_token': create_access_token(identity=idinfo['name']),
        'refresh_token': create_refresh_token(identity=idinfo['name'])
        }), 200

@app.route('/oicjob/api/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify({'access_token': create_access_token(identity=current_user)}), 200
