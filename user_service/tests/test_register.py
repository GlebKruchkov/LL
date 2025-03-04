import pytest
from flask import Flask
from api.register import register_blueprint
from db_functions import cleanup_database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(register_blueprint)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def cleanup_db():
    cleanup_database()

def test_register_success(client):
    data = {
        "login": "testuser",
        "password": "Password1!",
        "email": "test@example.com",
        "nickname": "testuser",
        "date_of_birth": "1990-01-01",
        "phone_number": "1234567890"
    }
    response = client.post('/api/v1/register', json=data)
    assert response.status_code == 200
    assert response.json == {"message": "User registered successfully"}

def test_register_missing_fields(client):
    data = {
        "login": "testuser",
        "password": "Password1!",
        "email": "test@example.com"
    }
    response = client.post('/api/v1/register', json=data)
    assert response.status_code == 400
    assert "Missing required fields" in response.json['error']

def test_register_duplicate_nickname(client):
    data = {
        "login": "testuser",
        "password": "Password1!",
        "email": "test@example.com",
        "nickname": "testuser",
        "date_of_birth": "1990-01-01",
        "phone_number": "1234567890"
    }
    client.post('/api/v1/register', json=data)
    response = client.post('/api/v1/register', json=data)
    assert response.status_code == 400
    assert "Nickname is already taken" in response.json['error']
