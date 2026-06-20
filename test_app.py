import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"DevOps Demo App Running Successfully!" in response.data

def test_health(client):
    """Test the health check route"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "UP"

def test_metrics(client):
    """Test the metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'flask_http_requests_total' in response.data
    assert b'flask_http_request_duration_seconds' in response.data

def test_invalid_route(client):
    """Test accessing an invalid route"""
    response = client.get('/invalid')
    assert response.status_code == 404

def test_app_context():
    """Test that app is created successfully"""
    assert app is not None
    assert app.config['TESTING'] == True