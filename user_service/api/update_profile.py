from flask import Blueprint, request, jsonify, abort, make_response
from datetime import datetime
from db_functions import update_user_profile, is_nickname_unique, create_table_users

update_profile_blueprint = Blueprint('update_profile', __name__)

@update_profile_blueprint.route('/api/v1/profile/<current_nickname>', methods=['PUT'])
def update_profile(current_nickname):
    create_table_users()
    data = request.json
    new_nickname = data.get('nickname')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number')

    if not all([new_nickname, date_of_birth, phone_number]):
        return make_response(jsonify({"error": "Missing required fields: nickname, date_of_birth, phone_number"}), 400)

    if not is_nickname_unique(new_nickname):
        return make_response(jsonify({"error": "Nickname is already taken"}), 400)

    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        return make_response(jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400)

    if not phone_number.isdigit():
        return make_response(jsonify({"error": "Phone number must contain only digits"}), 400)

    update_user_profile(current_nickname, new_nickname, date_of_birth, phone_number)

    return make_response(jsonify({"message": "Profile updated successfully"}), 200)
