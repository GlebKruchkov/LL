import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../user_service")))
from helpers import create_access_token
from flask import Blueprint, request, jsonify, abort, make_response
from db_functions import get_user_by_login, create_table_users, update_user_auth_token

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/api/v1/login', methods=['POST'])
def login():
    create_table_users()
    data = request.json
    login = data.get('login')
    password = data.get('password')

    if not all([login, password]):
        return make_response(jsonify({"error": "Missing required fields: login and password"}), 400)
    if len(login) < 3:
        return make_response(jsonify({"error": "Login must be at least 3 characters long"}), 400)

    if len(password) < 8:
        return make_response(jsonify({"error": "Password must be at least 8 characters long"}), 400)

    user = get_user_by_login(login)
    if not user or user[2] != password:
        return make_response(jsonify({"error": "Invalid login or password"}), 400)
    
    auth_token = create_access_token(data={"sub": login})

    return make_response(jsonify({
        "message": "Login successful",
        "user_id": user[0],
        "auth_token": auth_token
    }), 200)
