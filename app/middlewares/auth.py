from functools import wraps
from flask import request, abort
from app.config import Config

STATIC_API_KEY = Config.SECRET_API_KEY

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != STATIC_API_KEY:
            abort(401, description="Unauthorized: Invalid API key")
        return f(*args, **kwargs)
    return decorated_function
