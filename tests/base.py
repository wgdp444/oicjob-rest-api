from flask_testing import TestCase

from app import app
from auth import auth

from database import db, init_db

class BaseTestCase(TestCase):
  TOKEN = 4649
  def create_app(self):
    app.config.from_object('config.TestingConfig')
    return app

  def setUp(self):
    self.app = self.app.test_client()
    db.create_all()
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()