import os
import pytest
from app import create_app, db
from app.models import Patient

@pytest.fixture()
def client(tmp_path):
    os.environ['DATABASE_URL'] = 'sqlite:///' + str(tmp_path / 'test.db')
    os.environ['SECRET_KEY'] = 'test'
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Dashboard' in rv.data

def test_create_patient(client):
    # Create
    rv = client.post('/patients/new', data={
        'nhs_number': '1234567890',
        'full_name': 'Jane Doe',
        'date_of_birth': '1990-01-01'
    }, follow_redirects=True)
    assert b'Patient created successfully.' in rv.data
    # Read (list)
    rv = client.get('/patients?q=Jane')
    assert b'Jane Doe' in rv.data
