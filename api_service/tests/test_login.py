from unittest.mock import patch
import pytest
from api_service import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Login successful"}

        response = client.post(
            '/api/v1/login',
            json={"login": "testuser", "password": "testpass"}
        )

        assert response.status_code == 200
        assert "message" in response.json
        assert response.json["message"] == "Login successful"

        mock_post.assert_called_once_with(
            "http://user_service:5000/api/v1/login",
            json={"login": "testuser", "password": "testpass"}
        )

def test_login_failure(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "Invalid login or password"}

        response = client.post(
            '/api/v1/login',
            json={"login": "wronguser", "password": "wrongpass"}
        )

        assert response.status_code == 400
        assert "error" in response.json
        assert response.json["error"] == "Invalid login or password"

        mock_post.assert_called_once_with(
            "http://user_service:5000/api/v1/login",
            json={"login": "wronguser", "password": "wrongpass"}
        )
