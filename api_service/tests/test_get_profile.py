from unittest.mock import patch
import pytest
from api_service import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_profile_success(client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = ["", "", "", "", "testuser"]

        response = client.get('/api/v1/profile/testuser')
        assert response.status_code == 200
        assert response.json[4] == "testuser"

        mock_get.assert_called_once_with("http://user_service:5000/api/v1/profile/testuser")


def test_get_profile_failure(client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": "User not found"}

        response = client.get('/api/v1/profile/testuser')

        assert response.status_code == 404
        assert "User not found" in response.json['error']

        mock_get.assert_called_once_with("http://user_service:5000/api/v1/profile/testuser")