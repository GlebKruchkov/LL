from unittest.mock import patch
import pytest
from api_service import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_update_profile_success(client):
    with patch('requests.put') as mock_put:
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"message": "Profile updated successfully"}

        response = client.put(
            '/api/v1/profile/testuser',
            json = {
                "nickname": "new_nickname",
                "date_of_birth": "1991-01-01",
                "phone_number": "0987654321"
            }
        )

        assert response.status_code == 200
        assert "message" in response.json
        assert response.json["message"] == "Profile updated successfully"

        mock_put.assert_called_once_with(
            "http://user_service:5000/api/v1/profile/testuser",
            json = {
                "nickname": "new_nickname",
                "date_of_birth": "1991-01-01",
                "phone_number": "0987654321"
            }
        )

def test_update_profile_failure(client):
    with patch('requests.put') as mock_put:
        mock_put.return_value.status_code = 400
        mock_put.return_value.json.return_value = {"error": "Missing required fields: nickname, date_of_birth, phone_number"}

        response = client.put(
            '/api/v1/profile/testuser',
            json = {
                "nickname": "new_nickname"
            }
        )

        assert response.status_code == 400
        assert "error" in response.json
        assert response.json["error"] == "Missing required fields: nickname, date_of_birth, phone_number"

        mock_put.assert_called_once_with(
            "http://user_service:5000/api/v1/profile/testuser",
            json = {
                "nickname": "new_nickname"
            }
        )
