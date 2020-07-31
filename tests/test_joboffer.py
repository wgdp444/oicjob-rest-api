from .base import BaseTestCase
from auth import auth
from database import db
from models.models import JobOffer, Industry

import json
from parameterized import parameterized
import app
from unittest import mock
from flask_jwt_extended import create_access_token

USER_ID = '4649'
REQUEST_HEADERS = {
        'Content-Type': 'application/json;charset=utf-8',
        'Access-Control-Allow-Origin': 'http://127.0.0.1:4649',
        }

@mock.patch('auth.auth._google_oauth')
class TestJobOffer(BaseTestCase):
    def _init_header(self):
        ACCESS_TOKEN = create_access_token('testuser')
        return {
            'Content-Type': 'application/json;charset=utf-8',
            'Access-Control-Allow-Origin': 'http://127.0.0.1:4649',
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
    def test_create_joboffer(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        REQUEST_HEADERS = self._init_header()
        request_json = {
            'token': USER_ID,
            'company_name': '1',
            'industry_id': 1,
            'occupation': '1',
            'max_appicants': 1,
            'starting_salary': 1,
            'image_url_text': '1'
        }
        response = self.app.post('/oicjob/api/joboffer/create', headers=REQUEST_HEADERS, json=request_json)
        assert(json.loads(response.get_data()) == {'result': True})

    
    def test_get_joboffer(self, mock_google_oauth):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        REQUEST_HEADERS = self._init_header()
        db.session.add(JobOffer('1', 1, '1', 1, 1, '1'))
        # db.session.add(JobOffer('2', 2, 2, 2, 2, '2'))
        db.session.add(Industry(name='industry'))
        db.session.commit()

        request_json = {
            'token': USER_ID
        }
        response = self.app.post('/oicjob/api/joboffer/gets', headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())
        # 変動する時刻があるため項目ごとのテスト
        for joboffer in response_dict['joboffers']:
            assert joboffer['company_name'] == '1'
            assert joboffer['occupation'] == '1'
            assert joboffer['max_appicants'] == 1
            assert joboffer['starting_salary'] == 1
            assert joboffer['image_url_text'] == '1'
            assert type(joboffer['created']) == str
            assert type(joboffer['updated']) == str
            assert joboffer['created_by'] == 'system'
            assert joboffer['updated_by'] == 'system'
            for industry in joboffer['industry']:
                assert industry['name'] == 'industry'
    
    @parameterized.expand([
        (1, 204),
        (234, 500)
    ])
    def test_deleate_joboffer(self, mock_google_oauth, id, status_code):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        REQUEST_HEADERS = self._init_header()
        db.session.add(JobOffer('1', 1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
        }
        response = self.app.post(f'/oicjob/api/joboffer/delete/{id}', headers=REQUEST_HEADERS,json=request_json)
        assert(response.status_code == status_code)

    @parameterized.expand([
        (1, '1', 1, 1, 1, 1, '1', '1', 204),
        (3, '3', 3, 3, 3, 3, '3', '3', 500)
    ])
    def test_update_joboffer(self, mock_google_oauth, id, company_name, industry_id, occupation, max_appicants, starting_salary, image_url_text, updated_by, status_code):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        REQUEST_HEADERS = self._init_header()
        db.session.add(JobOffer('1', 1, 1, 1, 1, '1'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
            'company_name': company_name,
            'industry_id': industry_id,
            'occupation': occupation,
            'max_appicants': max_appicants,
            'starting_salary': starting_salary,
            'image_url_text': image_url_text,
            'updated_by': updated_by
        }
        response = self.app.post(f'/oicjob/api/joboffer/update/{id}', headers=REQUEST_HEADERS,json=request_json)
        assert(response.status_code == status_code)

    @parameterized.expand([
        ({'company_name': '1', 'updated_by': 'ninjadaizo'}, {'company_names': ('1', ), 'updated_bys': ('ninjadaizo', ), 'industry_id': (1, ), 'occupation': ('1', ), 'max_appicants': (1, )}),
        # ({'updated_by': 'ninjadaizo'}, {'names': ('息絶えた学科', 'テスト学科'), 'updated_bys': ('ninjadaizo', )}),
        # ({'updated_by': 'ほうじょうえいむ'}, {'names': ('1234', ), 'updated_bys': ('ほうじょうえいむ', )}),
        # ({'name': '息絶えた学科'}, {'names': ('息絶えた学科', ), 'updated_bys': ('ninjadaizo', )}),
    ])
    def test_search_subject(self, mock_google_oauth, search_condition, result):
        url = '/oicjob/api/joboffer/seartches'
        mock_google_oauth.return_value = {'sub': USER_ID}
        REQUEST_HEADERS = self._init_header()
        # テスト用データをcommit
        insert_datas = [{'company_name': '1', 'updated_by': 'ninjadaizo', 'industry_id': 1, 'occupation': 'エンジニア', 'max_appicants': 1, 'starting_salary': '300', 'image_url_text': 'test'},
                        {'company_name': '2', 'updated_by': 'ninjadaizo', 'industry_id': 1, 'occupation': '社畜', 'max_appicants': 2, 'starting_salary': '300', 'image_url_text': 'test'},
                        {'company_name': '3', 'updated_by': 'ikitaetayatsu', 'industry_id': 2, 'occupation': 'アイドル', 'max_appicants': 3, 'starting_salary': '300', 'image_url_text': 'test'},
                        {'company_name': '4', 'updated_by': 'ほうじょうえいむ', 'industry_id': 3, 'occupation': 'ほうじょうえいむ', 'max_appicants': 100, 'starting_salary': '300', 'image_url_text': 'test'},]
        test_records = []
        for insert_data in insert_datas:
            test_records.append(JobOffer(company_name=insert_data['company_name'], 
                                            updated_by=insert_data['updated_by'], 
                                            industry_id=insert_data['industry_id'],
                                            occupation=insert_data['occupation'],
                                            max_appicants=insert_data['max_appicants'],
                                            starting_salary=insert_data['starting_salary'],
                                            image_url_text=insert_data['image_url_text'],))
        db.session.bulk_save_objects(test_records)
        db.session.add(Industry(name='industry'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
        }
        request_json.update(search_condition)
        response = self.app.post(url, headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())
        for joboffer in response_dict['joboffers']:
            assert joboffer['company_name'] in result['company_names']
            assert joboffer['updated_by'] in result['updated_bys']
