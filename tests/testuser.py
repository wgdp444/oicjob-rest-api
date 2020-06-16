from .base import BaseTestCase

import json

from app import app

class TestUserAPI(BaseTestCase):
     def test_get_hoges_no_data(self):
        response = self.app.get('/test')
        self.assert_200(response)
        assert(
        json.loads(response.get_data()) == {'test': 'ok'}
        )