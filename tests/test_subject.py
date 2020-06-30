from .base import BaseTestCase
from auth import auth
from database import db
from models.models import Subject

import json
from parameterized import parameterized
import app
from unittest import mock

USER_ID = '4649'
REQUEST_HEADERS = {
        'Content-Type': 'application/json;charset=utf-8',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:4649'
        }

@mock.patch('auth.auth._google_oauth')
class TestSubject(BaseTestCase):
    def test_create_subject(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        request_json = {
            'token': USER_ID,
            'industry_id': 1,
            'occupation': 1,
            'max_appicants': 1,
            'starting_salary': 1,
            'image_url_text': '1'
        }
        response = self.app.post('/oicjob/api/create_subject', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': True})

    
    def test_get_subject(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(JobOffer(1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID
        }
        response = self.app.post('/oicjob/api/get_subject/all', headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())

        # 変動する時刻があるため項目ごとのテスト
        for subject in response_dict['subjects']:
            assert subject['industry_id'] == 1
            assert subject['occupation'] == 1
            assert subject['max_appicants'] == 1
            assert subject['starting_salary'] == 1
            assert subject['image_url_text'] == '1'
            assert type(subject['created']) == str
            assert type(subject['updated']) == str
            assert subject['created_by'] == 'system'
            assert subject['updated_by'] == 'system'

    
    @parameterized.expand([
        (1, True),
        (234, False)
    ])
    def test_deleate_subject(self, mock_google_oauth, id, result):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(JobOffer(1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
            'id': id
        }
        response = self.app.post('/oicjob/api/delete_subject', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': result})

    @parameterized.expand([
        (1, 1, 1, 1, 1, '1', True),
        (3, 3, 3, 3, 3, '3', False)
    ])
    def test_update_subject(self, mock_google_oauth, id, industry_id, occupation, max_appicants, starting_salary, image_url_text, result):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(JobOffer(1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
            'id': id,
            'industry_id': industry_id,
            'occupation': occupation,
            'max_appicants': max_appicants,
            'starting_salary': starting_salary,
            'image_url_text': image_url_text
        }
        response = self.app.post('/oicjob/api/delete_subject', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': result})