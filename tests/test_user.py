from .base import BaseTestCase
from auth import auth
from database import db
from models.models import User

import json
import app
from unittest import mock

USER_ID = '4649'
REQUEST_HEADERS = {
        'Content-Type': 'application/json;charset=utf-8',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:4649'
        }

class TestUser(BaseTestCase):
    def test_response_check(self):
        response = self.app.post('/oicjob/api/test')
        self.assert_200(response)
        assert(
        json.loads(response.get_data()) == {'result': 'ok'}
        )

    @mock.patch('auth.auth._google_oauth')
    def test_create_user(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        request_json = {
            'token': USER_ID,
            'subject_id': 1,
            'is_admin': False,
            'class_number': None,
        }
        response = self.app.post('/oicjob/api/create_user', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': True})

    @mock.patch('auth.auth._google_oauth')
    def test_get_user(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(User(USER_ID, 1, False, class_number=1))
        db.session.commit()

        request_json = {
            'token': USER_ID
        }
        response = self.app.post('/oicjob/api/get_user', headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())

        # assert(json.loads(response.get_data()) == {'result': True})

        # 変動する時刻があるため項目ごとのテスト
        assert response_dict['google_id'] == USER_ID
        assert response_dict['class_number'] == 1
        assert response_dict['is_admin'] == False
        assert response_dict['subject_id'] == 1
        assert response_dict['created_by'] == 'system'
        assert type(response_dict['created']) == str