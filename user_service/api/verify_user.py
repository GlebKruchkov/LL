from flask import Blueprint, make_response, request, jsonify
from helpers import get_current_user, AuthError

verify_blueprint = Blueprint('verify', __name__)

@verify_blueprint.route('/api/v1/users/verify', methods=['GET'])
def verify_user():
    auth_token = request.headers.get('X-Auth-Token')
    if not auth_token:
        return jsonify({"error": "Token missing"}), 401

    try:
        user = get_current_user(auth_token)
        return jsonify(user), 200
        
    except AuthError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
