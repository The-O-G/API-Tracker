from functools import wraps
import requests
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != os.getenv("MY_SECRET_KEY"):
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)
    return decorated
