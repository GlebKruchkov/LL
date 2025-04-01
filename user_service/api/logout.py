from flask import Blueprint, make_response, request, jsonify
from db_functions import update_user_auth_token

logout_blueprint = Blueprint('logout', __name__)

@logout_blueprint.route('/api/v1/logout', methods=['POST'])
def logout():
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        return make_response(jsonify({"error": "User ID missing"}), 400)

    update_user_auth_token(user_id, None)

    return make_response(jsonify({"message": "Logged out successfully"}), 200)
