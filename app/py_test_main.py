import os
import tempfile

from app import app
import pytest

@pytest.fixture
def client():
    db_fd,app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True 
    with app.test_client() as client:
        #with app.app_context():
        #    app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_1(client):
    rv = client.get('/create_account')
    assert b'aaaaaa' in rv.data


