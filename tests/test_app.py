import pytest
from app import app, get_token

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
def auth_token(client):
    response = client.get('/token')
    return response.json['token']

def test_authorization(client):
    response = client.get('/cpu', headers={'Authorization': 'dummy-header'})
    assert response.status_code == 401
    response = client.get('/cpu')
    assert response.status_code == 403 # Forbidden if no token

def test_get_cpu_usage(client):
    response = client.get('/cpu', headers={'Authorization': auth_token(client)})
    assert response.status_code == 200

def test_get_memory_usage(client):
    response = client.get('/memory', headers={'Authorization': auth_token(client)})
    assert response.status_code == 200

def test_get_disk_usage(client):
    response = client.get('/disk', headers={'Authorization': auth_token(client)})
    assert response.status_code == 200

def test_get_bandwidth_usage(client):
    response = client.get('/bandwidth', headers={'Authorization': auth_token(client)})
    assert response.status_code == 200

def test_get_token(client):
    response = client.get('/token')
    assert response.status_code == 200
    assert 'token' in response.json
