from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from controller import login, user, subject, joboffer
from database import init_db
import traceback

# init
app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)
init_db(app)

# BluePrint
app.register_blueprint(login.app)
app.register_blueprint(user.app)
app.register_blueprint(subject.app)
app.register_blueprint(joboffer.app)

@app.errorhandler(403)
def forbidden(e):
    return jsonify({'result': 'forbidden'})

@app.errorhandler(404)
def not_found(e):
    return jsonify({'result': 'not found'})

@app.route('/oicjob/api/test',methods=["POST"])
def test():
    return jsonify({'test': 'ok'})

# @app.errorhandler(Exception)
# def api_error(e):
#     print(e.args)
#     return jsonify({'result': 'api error'}), 500

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=4649)