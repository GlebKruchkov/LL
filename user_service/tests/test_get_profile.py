import pytest
from flask import Flask
from api.get_profile import get_profile_blueprint
from db_functions import insert_into_users, create_table_users

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(get_profile_blueprint)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_profile_success(client):
    create_table_users()
    insert_into_users("testuser", "Password1!", "test@example.com", "testuser", "1990-01-01", "1234567890")
    response = client.get('/api/v1/profile/testuser')
    assert response.status_code == 200
    assert response.json[4] == "testuser"

def test_get_profile_not_found(client):
    response = client.get('/api/v1/profile/nonexistent')
    assert response.status_code == 404
    assert "User not found" in response.json['error']
