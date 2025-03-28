from unittest.mock import patch
import pytest
from api_service import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_success(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "User registered successfully"}

        response = client.post(
            '/api/v1/register',
            json = {
                "login": "testuser",
                "password": "Password1!",
                "email": "test@example.com",
                "nickname": "testuser",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            }
        )

        assert response.status_code == 200
        assert "message" in response.json
        assert response.json["message"] == "User registered successfully"

        mock_post.assert_called_once_with(
            "http://user_service:5000/api/v1/register",
            json = {
                "login": "testuser",
                "password": "Password1!",
                "email": "test@example.com",
                "nickname": "testuser",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            }
        )

def test_register_failure(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "Nickname is already taken"}

        response = client.post(
            '/api/v1/register',
            json = {
                "login": "testuser",
                "password": "Password1!",
                "email": "test@example.com",
                "nickname": "testuser",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            }
        )

        assert response.status_code == 400
        assert "error" in response.json
        assert response.json["error"] == "Nickname is already taken"

        mock_post.assert_called_once_with(
            "http://user_service:5000/api/v1/register",
            json = {
                "login": "testuser",
                "password": "Password1!",
                "email": "test@example.com",
                "nickname": "testuser",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            }
        )
