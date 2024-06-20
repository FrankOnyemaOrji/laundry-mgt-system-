from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus

from ..models.admin import Admin


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jwt_token = request.headers.get('Authorization', None)
        # print(f"JWT Token: {jwt_token}")  # Print the JWT token
        current_user_id = get_jwt_identity()
        # print(f"User ID from JWT: {current_user_id}")  # Print the result of get_jwt_identity
        if current_user_id is None:
            return {"message": "User ID from JWT is None"}, HTTPStatus.INTERNAL_SERVER_ERROR
        current_user = Admin.query.filter_by(id=current_user_id).first()
        if current_user is None or current_user.user_type != "admin":
            return {"message": "Admins only!"}, HTTPStatus.FORBIDDEN
        return fn(*args, **kwargs)
    return wrapper
