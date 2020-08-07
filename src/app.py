from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from controller import login, user, subject, joboffer, pdf, industry, area
from database import init_db
import traceback
from datetime import timedelta

# init
app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)
init_db(app)
app.config['JWT_SECRET_KEY'] = 'test'  # Change this!
# jwt有効時間
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=3)
jwt = JWTManager(app)

# BluePrint
app.register_blueprint(login.app)
app.register_blueprint(user.app)
app.register_blueprint(subject.app)
app.register_blueprint(joboffer.app)
app.register_blueprint(pdf.app)
app.register_blueprint(industry.app)
app.register_blueprint(area.app)

@app.errorhandler(403)
def forbidden(e):
    return jsonify({'result': 'forbidden'}), 403

@app.errorhandler(404)
def not_found(e):
    return jsonify({'result': 'not found'})

@app.route('/oicjob/api/test',methods=["POST"])
def test():
    return jsonify({'result': 'ok'})

@app.errorhandler(Exception)
def api_error(e):
    print(traceback.format_exc())
    return jsonify({'result': 'api error'})

@app.after_request
def after_request(response):
    # application/jsonで204を返すための処理
    # 参照: https://www.erol.si/2018/03/flask-return-204-no-content-response/
    if response.status_code == 204:
        response.mimetype = app.config['JSONIFY_MIMETYPE']
    return response


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=4649)