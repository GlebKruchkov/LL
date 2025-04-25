import base64
from datetime import datetime, timedelta
import hashlib
import hmac
from flask import abort
from flask import json
from db_functions import get_user_by_login, create_table_users

SECRET_KEY = "your_secret_key"
EXPIRATION_TIME = 900

class AuthError(Exception):
    def __init__(self, message, status_code=401):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

def encode_base64(data: dict) -> str:
    json_data = json.dumps(data, separators=(",", ":"))
    return base64.urlsafe_b64encode(json_data.encode()).decode().strip("=")

def decode_base64(encoded_data: str) -> dict:
    try:
        padding = "=" * (4 - len(encoded_data) % 4)
        data = base64.urlsafe_b64decode(encoded_data + padding).decode()
        return json.loads(data)
    except Exception:
        raise AuthError("Invalid token format")

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=EXPIRATION_TIME))
    to_encode.update({"exp": expire.isoformat()})
    
    encoded_header = encode_base64({"alg": "HS256", "typ": "JWT"})
    encoded_payload = encode_base64(to_encode)
    
    message = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()

    return f"{encoded_header}.{encoded_payload}.{signature}"

def decode_access_token(token: str) -> dict:
    if not token or token.count('.') != 2:
        raise AuthError("Invalid token format", 401)
    
    try:
        header_b64, payload_b64, signature = token.split('.')
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            raise AuthError("Invalid token signature", 401)
            
        payload = decode_base64(payload_b64)
        
        if datetime.fromisoformat(payload["exp"]) < datetime.utcnow():
            raise AuthError("Token expired", 401)
            
        return payload
    except json.JSONDecodeError:
        raise AuthError("Invalid token payload", 401)
    except Exception:
        raise AuthError("Invalid token", 401)

def get_current_user(token: str):
    if not token:
        raise AuthError("Token missing")
    
    try:
        payload = decode_access_token(token)
        login = payload.get("sub")
        if not login:
            raise AuthError("Invalid token payload")
        user = get_user_by_login(login)
        if not user:
            raise AuthError("User not found", 404)

        return user
    except AuthError:
        raise
    except Exception:
        raise AuthError("Invalid token")
