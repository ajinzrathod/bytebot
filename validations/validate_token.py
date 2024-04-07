from functools import wraps
from flask import request, jsonify


def validate_token(ask_token):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or token != f"Bearer {ask_token}":
                return jsonify({"message": "Unauthorized"}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator
