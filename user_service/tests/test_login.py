import pytest
from flask import Flask
from api.login import login_blueprint
from db_functions import insert_into_users, create_table_users, cleanup_database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(login_blueprint)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def cleanup_db():
    cleanup_database()

def test_login_success(client):
    create_table_users()
    insert_into_users("testuser", "Password1!", "test@example.com", "testuser", "1990-01-01", "1234567890")
    data = {
        "login": "testuser",
        "password": "Password1!"
    }
    response = client.post('/api/v1/login', json=data)
    assert response.status_code == 200
    assert response.json == {"message": "Login successful"}

def test_login_invalid_credentials(client):
    data = {
        "login": "testuser",
        "password": "WrongPassword"
    }
    response = client.post('/api/v1/login', json=data)
    assert response.status_code == 400
    assert "Invalid login or password" in response.json['error']
