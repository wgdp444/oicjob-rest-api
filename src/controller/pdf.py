import json
import os
import traceback
import base64
import werkzeug
from datetime import datetime


from flask import Blueprint, jsonify, request, abort, make_response
from flask_jwt_extended import jwt_required


from models.models import Subject
from auth.auth import default_auth
from database import db
from controller.modules import common


app = Blueprint('pdf', __name__)

MAX_JSON_CONTENT_LENGTH = int(os.getenv("MAX_JSON_CONTENT_LENGTH", default="1048576"))
UPLOAD_DIR = '../pdf/'

# @app.route('/oicjob/api/pdf/upload',methods=["POST"])
# def upload_pdf():
#     decoded_content_data = base64.b64decode(request.json['content_data'])
#     if MAX_JSON_CONTENT_LENGTH > 0:
#         if content_length := len(decoded_content_data) > MAX_JSON_CONTENT_LENGTH:
#             raise werkzeug.exceptions.RequestEntityTooLarge(f'json content length over : {content_length}')


