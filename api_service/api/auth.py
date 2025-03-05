from flask import Blueprint, jsonify, request
import requests

auth_blueprint = Blueprint('auth', __name__)

USER_SERVICE_URL = "http://user_service:5000"

@auth_blueprint.route('/api/v1/register', methods=['POST'])
def register():
    response = requests.post(f"{USER_SERVICE_URL}/api/v1/register", json=request.json)
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

@auth_blueprint.route('/api/v1/login', methods=['POST'])
def login():
    response = requests.post(f"{USER_SERVICE_URL}/api/v1/login", json=request.json)
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code
