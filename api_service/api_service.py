from flask import Flask, jsonify, request
import requests
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

API_URL = '/static/openapi.yml'

SWAGGER_URL = '/api/docs'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Authentication API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

USER_SERVICE_URL = "http://user_service:5000"

@app.route('/api/v1/register', methods=['POST'])
def register():
    response = requests.post(f"{USER_SERVICE_URL}/api/v1/register", json=request.json)
    
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code


@app.route('/api/v1/login', methods=['POST'])
def login():
    response = requests.post(f"{USER_SERVICE_URL}/api/v1/login", json=request.json)
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

@app.route('/api/v1/profile/<nickname>', methods=['PUT'])
def update_profile(nickname):
    response = requests.put(f"{USER_SERVICE_URL}/api/v1/profile/{nickname}", json=request.json)
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

@app.route('/api/v1/profile/<nickname>', methods=['GET'])
def get_profile(nickname):
    response = requests.get(f"{USER_SERVICE_URL}/api/v1/profile/{nickname}")
    try:
        return jsonify(response.json()), response.status_code
    except requests.exceptions.JSONDecodeError:
        return response.text, response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
