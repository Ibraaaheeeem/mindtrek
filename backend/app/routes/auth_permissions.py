from flask import request, abort, jsonify
from functools import wraps
import app
import jwt

ALGORITHMS = ['RS256']

class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split(' ')
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def verify_decode_jwt(token):
    try:
        decoded_payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=ALGORITHMS)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.DecodeError:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Invalid token.'
        }, 401)

def requires_auth():
    """
    Decorator to require authentication
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator