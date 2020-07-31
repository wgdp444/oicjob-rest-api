import os
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../oicjob.db')
test_databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../test_oicjob.db')

class DevelopmentConfig:

  user = os.environ.get('DB_USER', default='root')
  host = os.environ.get('DB_HOST', default='test_mysql_container')
  db_name = os.environ.get('DB_NAME', default='test')

  # SQLAlchemy testDB
  SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:mysql@{host}/{db_name}?charset=utf8'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False

class TestingConfig:

  # # SQLAlchemy
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + test_databese_file
  # MySQL 
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@test_mysql_container/pytest?charset=utf8'
  TESTING = True


Config = DevelopmentConfig