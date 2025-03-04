from flask import Blueprint, request, jsonify, abort, make_response
from db_functions import get_user_by_login, create_table_users

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

    return make_response(jsonify({"message": "Login successful"}), 200)
