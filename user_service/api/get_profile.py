from flask import Blueprint, jsonify, make_response
from db_functions import get_user_by_nickname, create_table_users

get_profile_blueprint = Blueprint('get_profile', __name__)

@get_profile_blueprint.route('/api/v1/profile/<nickname>', methods=['GET'])
def get_profile(nickname):
    create_table_users()
    if len(nickname) < 3:
        return make_response(jsonify({"error": "Nickname must be at least 3 characters long"}), 400)

    user = get_user_by_nickname(nickname)
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    return jsonify(user), 200
