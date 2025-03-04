from flask import Blueprint, make_response, request, jsonify, abort
import re
from db_functions import (
    create_table_users,
    insert_into_users,
    is_nickname_unique,
    is_login_unique,
    is_email_unique
)

register_blueprint = Blueprint('register', __name__)

def is_email_valid(email):
    return "@" in email

def is_password_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@register_blueprint.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')
    nickname = data.get('nickname')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number')

    if not all([login, password, email, nickname, date_of_birth, phone_number]):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    create_table_users()

    if not is_nickname_unique(nickname):
        return make_response(jsonify({"error": "Nickname is already taken"}), 400)

    if not is_login_unique(login):
        return make_response(jsonify({"error": "Login is already taken"}), 400)

    if not is_email_unique(email):
        return make_response(jsonify({"error": "Email is already registered"}), 400)

    if not is_email_valid(email):
        return make_response(jsonify({"error": "Invalid email format"}), 400)

    if not is_password_strong(password):
        return make_response(jsonify({"error": "Password is too weak. "
                                      "It must be at least 8 characters long, contain a digit,"
                                      "an uppercase letter, and a special character."}), 400)

    insert_into_users(login, password, email, nickname, date_of_birth, phone_number)

    return make_response(jsonify({"message": "User registered successfully"}), 200)
