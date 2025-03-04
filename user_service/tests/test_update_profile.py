import pytest
from flask import Flask
from api.update_profile import update_profile_blueprint
from db_functions import insert_into_users, create_table_users, cleanup_database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(update_profile_blueprint)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def cleanup_db():
    cleanup_database()

def test_update_profile_success(client):
    create_table_users()
    insert_into_users("testuser", "Password1!", "test@example.com", "testuser", "1990-01-01", "1234567890")
    data = {
        "nickname": "new_nickname",
        "date_of_birth": "1991-01-01",
        "phone_number": "0987654321"
    }
    response = client.put('/api/v1/profile/testuser', json=data)
    assert response.status_code == 200
    assert "Profile updated successfully" in response.json['message']

def test_update_profile_missing_fields(client):
    data = {
        "nickname": "new_nickname"
    }
    response = client.put('/api/v1/profile/testuser', json=data)
    assert response.status_code == 400
    assert "Missing required fields: nickname, date_of_birth, phone_number" in response.json['error']
