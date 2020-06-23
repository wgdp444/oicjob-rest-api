from .base import BaseTestCase
from auth import auth
from database import db
from models.models import JobOffer

import json
import app
from unittest import mock

USER_ID = '4649'
REQUEST_HEADERS = {
        'Content-Type': 'application/json;charset=utf-8',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:4649'
        }

class TestJobOffer(BaseTestCase):
    @mock.patch('auth.auth._google_oauth')
    def test_create_joboffer(self, mock_google_oauth):
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
        response = self.app.post('/oicjob/api/create_joboffer', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': True})

    @mock.patch('auth.auth._google_oauth')
    def test_get_joboffer(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(JobOffer(1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID
        }
        response = self.app.post('/oicjob/api/get_joboffer/all', headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())

        # assert(json.loads(response.get_data()) == {'result': True})

        # 変動する時刻があるため項目ごとのテスト
        for joboffer in response_dict['joboffers']:
            assert joboffer['industry_id'] == 1
            assert joboffer['occupation'] == 1
            assert joboffer['max_appicants'] == 1
            assert joboffer['starting_salary'] == 1
            assert joboffer['image_url_text'] == '1'
            assert type(joboffer['created']) == str
            assert type(joboffer['updated']) == str
            assert joboffer['created_by'] == 'system'
            assert joboffer['updated_by'] == 'system'