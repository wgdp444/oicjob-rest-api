import os
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../oicjob.db')
test_databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../test_oicjob.db')

class DevelopmentConfig:

  # SQLAlchemy
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + databese_file
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False

class TestingConfig:

  # SQLAlchemy
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + test_databese_file
  TESTING = True


Config = DevelopmentConfig