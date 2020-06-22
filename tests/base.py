from flask_testing import TestCase

from app import api

from database import db, init_db


class BaseTestCase(TestCase):
  def create_app(self):
    api.config.from_object('config.TestingConfig')
    return api

  def setUp(self):
    self.app = self.app.test_client()
    db.create_all()
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()