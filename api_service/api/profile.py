from flask import Blueprint, jsonify, request
import requests

profile_blueprint = Blueprint('profile', __name__)

USER_SERVICE_URL = "http://user_service:5000"

@profile_blueprint.route('/api/v1/profile/<nickname>', methods=['PUT'])
def update_profile(nickname):
    response = requests.put(f"{USER_SERVICE_URL}/api/v1/profile/{nickname}", json=request.json)
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

@profile_blueprint.route('/api/v1/profile/<nickname>', methods=['GET'])
def get_profile(nickname):
    response = requests.get(f"{USER_SERVICE_URL}/api/v1/profile/{nickname}")
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

@profile_blueprint.route('/api/v1/users/verify', methods=['GET'])
def verify():
    headers = {'X-Auth-Token': request.headers.get('X-Auth-Token', '')}
    response = requests.get(
        f"{USER_SERVICE_URL}/api/v1/users/verify",
        headers=headers
    )
    return jsonify(response.json()), response.status_code

@profile_blueprint.route('/api/v1/logout', methods=['POST'])
def logout():
    headers = {'X-User-Id': request.headers.get('X-User-Id', '')}
    response = requests.post(
        f"{USER_SERVICE_URL}/api/v1/logout",
        headers=headers
    )

    return jsonify(response.json()), response.status_code
