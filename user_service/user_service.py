from flask import Flask, abort, jsonify, request
import re
from datetime import datetime
from db_functions import (
    create_table_users,
    insert_into_users,
    get_user_by_login,
    update_user_profile,
    get_user_by_nickname,
    is_nickname_unique,
    is_login_unique,
    is_email_unique
)

app = Flask(__name__)


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


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')
    nickname = data.get('nickname')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number')

    if not all([login, password, email, nickname, date_of_birth, phone_number]):
        abort(400, description="Missing required fields")

    create_table_users()

    if not is_nickname_unique(nickname):
        abort(400, description="Nickname is already taken")

    if not is_login_unique(login):
        abort(400, description="Login is already taken")

    if not is_email_unique(email):
        abort(400, description="Email is already registered")

    if not is_email_valid(email):
        abort(400, description="Invalid email format")

    if not is_password_strong(password):
        abort(400, description="Password is too weak. It must be at least 8 characters long, contain a digit, an uppercase letter, and a special character.")

    insert_into_users(login, password, email, nickname, date_of_birth, phone_number)

    return jsonify({"message": "User registered successfully"}), 200


@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    if not all([login, password]):
        abort(400, description="Missing required fields: login and password")

    if len(login) < 3:
        abort(400, description="Login must be at least 3 characters long")

    if len(password) < 8:
        abort(400, description="Password must be at least 8 characters long")

    user = get_user_by_login(login)
    if not user or user[2] != password:
        abort(400, description="Invalid login or password")

    return jsonify({"message": "Login successful", "user_id": user[0]}), 200


@app.route('/api/v1/profile/<current_nickname>', methods=['PUT'])
def update_profile(current_nickname):
    data = request.json
    new_nickname = data.get('nickname')
    date_of_birth = data.get('date_of_birth')
    phone_number = data.get('phone_number')

    if not all([new_nickname, date_of_birth, phone_number]):
        abort(400, description="Missing required fields: nickname, date_of_birth, phone_number")

    if not is_nickname_unique(new_nickname):
        abort(400, description="Nickname is already taken")

    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DD")

    if not phone_number.isdigit():
        abort(400, description="Phone number must contain only digits")

    update_user_profile(current_nickname, new_nickname, date_of_birth, phone_number)

    return jsonify({"message": "Profile updated successfully"}), 200


@app.route('/api/v1/profile/<nickname>', methods=['GET'])
def get_profile(nickname):
    if len(nickname) < 3:
        abort(400, description="Nickname must be at least 3 characters long")

    user = get_user_by_nickname(nickname)
    if not user:
        abort(404, description="User not found")

    return jsonify(user), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
