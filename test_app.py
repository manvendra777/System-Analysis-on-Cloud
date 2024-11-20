import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
def test_authorization(client):
    response = client.get('/cpu', headers={'Authorization': 'dummy-header'})
    assert response.status_code == 401
    response = client.get('/cpu')
    assert response.status_code == 403 # Forbidden if no token

def test_get_cpu_usage(client):
    response = client.get('/cpu', headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwOTQwOTV9.pTMdQvQrm7GjvxzalwzFKBMjl1UKaBLckDb7A7jPkvc'})
    assert response.status_code == 200

def test_get_memory_usage(client):
    response = client.get('/memory', headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwOTQwOTV9.pTMdQvQrm7GjvxzalwzFKBMjl1UKaBLckDb7A7jPkvc'})
    assert response.status_code == 200

def test_get_disk_usage(client):
    response = client.get('/disk', headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwOTQwOTV9.pTMdQvQrm7GjvxzalwzFKBMjl1UKaBLckDb7A7jPkvc'})
    assert response.status_code == 200

def test_get_bandwidth_usage(client):
    response = client.get('/bandwidth', headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzIwOTQwOTV9.pTMdQvQrm7GjvxzalwzFKBMjl1UKaBLckDb7A7jPkvc'})
    assert response.status_code == 200

def test_get_token(client):
    response = client.get('/token')
    assert response.status_code == 200
    assert 'token' in response.json
