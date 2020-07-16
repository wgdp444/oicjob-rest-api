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
    # TODO: 失敗時の処理
    @parameterized.expand([
        ('息絶えた学科', True),
    ])
    def test_create_subject(self, mock_google_oauth, name, result):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        request_json = {
            'token': USER_ID,
            'name': name
        }
        response = self.app.post('/oicjob/api/create_subject', headers=REQUEST_HEADERS,json=request_json)
        assert(json.loads(response.get_data()) == {'result': result})

    @parameterized.expand([
        (1, ),
        (234, ),
    ])
    def test_get_subject(self, mock_google_oauth, id):
        # 認証回避のmock
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(Subject('息絶えた学科'))
        db.session.add(Subject('忍者学科'))
        db.session.commit()

        request_json = {
            'token': USER_ID
        }
        response = self.app.post('/oicjob/api/subject/get', headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())
        # all
        # 変動する時刻があるため項目ごとのテスト
        for subject in response_dict['subjects']:
            assert subject['name'] in ('息絶えた学科', '忍者学科', )
            assert type(subject['created']) == str
            assert type(subject['updated']) == str
            assert subject['created_by'] == 'system'
            assert subject['updated_by'] == 'system'
        
        # TODO: id指定の単体処理

    
    @parameterized.expand([
        (1, 204),
        (234, 400),
    ])
    def test_deleate_subject(self, mock_google_oauth, id, status_code):
        # 認証回避のmock
        url = f'/oicjob/api/subject/delete/{str(id)}'
        print(url)
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(Subject('息絶えた学科'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
        }
        response = self.app.post(url, headers=REQUEST_HEADERS,json=request_json)
        assert(response.status_code == status_code)

    @parameterized.expand([
        (1, {'name': 'テスト学科', 'updated_by': 'ninjadaizo'}, {'name': 'テスト学科', 'updated_by': 'ninjadaizo'}, 204),
        (234, {'name': 'テスト学科', 'updated_by': 'ninjadaizo'}, {'name': None, 'updated_by': None}, 400)
    ])
    def test_update_subject(self, mock_google_oauth, id, inputs, results, status_code):
        # 認証回避のmock
        url = f'/oicjob/api/subject/update/{str(id)}'
        mock_google_oauth.return_value = {'sub': USER_ID}
        db.session.add(Subject('息絶えた学科'))
        db.session.commit()

        request_json = {
            'token': USER_ID,
            'name': inputs['name'],
            'updated_by': inputs['updated_by'],
        }

        response = self.app.post(url, headers=REQUEST_HEADERS,json=request_json)
        assert(response.status_code == status_code)

        subject = Subject.query.filter_by(id=id).first()
        if subject is not None:
            assert subject.name == results['name']
            assert subject.updated_by == results['updated_by']
        

    @parameterized.expand([
        ({'name': '息絶えた学科'}, {'names': ('息絶えた学科', ), 'updated_bys': ('ninjadaizo', )}),
        ({'updated_by': 'ninjadaizo'}, {'names': ('息絶えた学科', 'テスト学科'), 'updated_bys': ('ninjadaizo', )}),
        ({'updated_by': 'ほうじょうえいむ'}, {'names': ('1234', ), 'updated_bys': ('ほうじょうえいむ', )}),
        ({'name': '息絶えた学科'}, {'names': ('息絶えた学科', ), 'updated_bys': ('ninjadaizo', )}),
    ])
    def test_search_subject(self, mock_google_oauth, search_condition, result):
        url = '/oicjob/api/subject/seartches'
        mock_google_oauth.return_value = {'sub': USER_ID}
        insert_names = ['息絶えた学科', 'テスト学科', 'DragonBorn', '1234']
        insert_updated_bys = ['ninjadaizo', 'ninjadaizo', 'ikitaetayatsu', 'ほうじょうえいむ']
        test_records = []
        for name, updated_by in zip(insert_names, insert_updated_bys):
            test_records.append(Subject(name=name, updated_by=updated_by))
        db.session.bulk_save_objects(test_records)
        db.session.commit()

        request_json = {
            'token': USER_ID,
        }
        request_json.update(search_condition)
        response = self.app.post(url, headers=REQUEST_HEADERS,json=request_json)
        response_dict = json.loads(response.get_data())

        for subject in response_dict['subjects']:
            assert subject['name'] in result['names']
            assert subject['updated_by'] in result['updated_bys']