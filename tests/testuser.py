from .base import BaseTestCase

import json

import app

class TestUser(BaseTestCase):
     def test_response_check(self):
        response = self.app.post('/oicjob/api/test')
        self.assert_200(response)
        assert(
        json.loads(response.get_data()) == {'test': 'ok'}
        )