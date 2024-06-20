from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from ..models.admin import Admin
from ..utils.decorator import admin_required

admin_namespace = Namespace("admin", description="Admin related operations")

admin_model = admin_namespace.model(
    "Admin",
    {
        "id": fields.String(required=True, description="Admin ID"),
        "firstName": fields.String(required=True, description="Admin First Name"),
        "lastName": fields.String(required=True, description="Admin Last Name"),
        "email": fields.String(required=True, description="Admin Email"),
        "password_hash": fields.String(required=True, description="Admin Password"),
        "phone_Number": fields.String(required=True, description="Admin Phone Number"),
        "user_type": fields.String(required=True, description="Admin User Type"),
    },
)

login_model = admin_namespace.model(
    "Login",
    {
        "email": fields.String(required=True, description="Admin Email"),
        "password": fields.String(required=True, description="Admin Password"),
    },
)

register_model = admin_namespace.model(
    "Register",
    {
        "firstName": fields.String(required=True, description="Admin First Name"),
        "lastName": fields.String(required=True, description="Admin Last Name"),
        "email": fields.String(required=True, description="Admin Email"),
        "password": fields.String(required=True, description="Admin Password"),
        "phone_Number": fields.String(required=True, description="Admin Phone Number"),
    },
)


@admin_namespace.route("/register")
class Register(Resource):
    @admin_namespace.expect(register_model)
    @admin_namespace.doc(description="Register a new admin")
    def post(self):
        """ Register a new admin """
        data = admin_namespace.payload
        admin = Admin.query.filter_by(email=data["email"]).first()
        if admin:
            return {"message": "Admin already exists"}, HTTPStatus.CONFLICT
        new_admin = Admin(
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
            phone_Number=data["phone_Number"],
        )
        new_admin.save()
        admin_response = {
            "id": new_admin.id,
            "firstName": new_admin.firstName,
            "lastName": new_admin.lastName,
            "email": new_admin.email,
            "phone_Number": new_admin.phone_Number,
            "user_type": new_admin.user_type,
        }
        return admin_response, HTTPStatus.CREATED


@admin_namespace.route("/login")
class Login(Resource):
    @admin_namespace.expect(login_model)
    @admin_namespace.doc(description="Login an admin")
    def post(self):
        """ Login an admin """
        data = admin_namespace.payload
        email = data["email"]
        password = data["password"]
        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            return {"message": "Admin not found"}, HTTPStatus.NOT_FOUND
        if not check_password_hash(admin.password_hash, password):
            return {"message": "Invalid password"}, HTTPStatus.UNAUTHORIZED
        if admin.id is None:
            return {"message": "Admin ID is None"}, HTTPStatus.INTERNAL_SERVER_ERROR
        access_token = create_access_token(identity=admin.id, fresh=True)
        refresh_token = create_refresh_token(identity=admin.id)
        # print(f"Access Token: {access_token}")
        # print(f"Refresh Token: {refresh_token}")
        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response, HTTPStatus.OK


@admin_namespace.route("/update_admin_details/<string:admin_id>")
class UpdateAdminDetails(Resource):
    @admin_namespace.expect(register_model)
    @admin_namespace.doc(description="Update admin details")
    @jwt_required()
    @admin_required
    def patch(self, admin_id):
        """ Update admin details """
        admin = Admin.get_by_id(admin_id)
        active_admin = get_jwt_identity()
        if admin.id != active_admin:
            return {"message": "Unauthorized"}, HTTPStatus.FORBIDDEN
        data = admin_namespace.payload
        admin.firstName = data["firstName"]
        admin.lastName = data["lastName"]
        admin.email = data["email"]
        admin.password_hash = generate_password_hash(data["password"])
        admin.phone_Number = data["phone_Number"]
        admin.update()
        admin_response = {
            "id": admin.id,
            "firstName": admin.firstName,
            "lastName": admin.lastName,
            "email": admin.email,
            "phone_Number": admin.phone_Number,
            "user_type": admin.user_type,
        }
        return admin_response, HTTPStatus.OK

