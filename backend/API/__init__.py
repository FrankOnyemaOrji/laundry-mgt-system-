from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus
from dotenv import load_dotenv

from .config.config import config_dict
from .utils import db
from .utils.blacklist import BLACKLIST
from .auth.auth_view import auth_namespace
from .admin.admin_view import admin_namespace
from .orders.order_view import order_namespace

from .models.admin import Admin
from .models.users import User
from .models.order import Order


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    load_dotenv()
    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLACKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            "message": "Token has expired or been revoked",
            "error": "token_expired",
        }

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token",
        }, HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required",
        }, HTTPStatus.UNAUTHORIZED

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(j):
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required",
        }, HTTPStatus.UNAUTHORIZED

    @jwt.expired_token_loader
    def expired_token_callback(j):
        return {
            "message": "The token has expired",
            "error": "token_expired",
        }, HTTPStatus.UNAUTHORIZED

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with **Bearer &lt;JWT&gt;** token to authorize the request",
        }
    }

    api = Api(
        app,
        title="Laundry Management System API",
        description="A simple API for Laundry Management System",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(order_namespace, path="/order")

    @app.errorhandler(NotFound)
    def not_found(error):
        return {
            "message": "Resource not found",
            "error": "not_found",
        }, HTTPStatus.NOT_FOUND

    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {
            "message": "Method not allowed",
            "error": "method_not_allowed",
        }, HTTPStatus.METHOD_NOT_ALLOWED

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Admin": Admin,
            "User": User,
        }

    return app
