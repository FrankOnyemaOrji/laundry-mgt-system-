from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

from ..models.users import User
from ..utils.decorator import admin_required
from ..utils.blacklist import BLACKLIST

auth_namespace = Namespace('auth', description='Authentication')

user_model = auth_namespace.model(
    'User',
    {
        'id': fields.String(required=True, description='User ID'),
        'firstName': fields.String(required=True, description='User First Name'),
        'lastName': fields.String(required=True, description='User Last Name'),
        'email': fields.String(required=True, description='User Email'),
        'password_hash': fields.String(required=True, description='User Password'),
        'phone_Number': fields.String(required=True, description='User Phone Number'),
        'user_type': fields.String(required=True, description='User Type'),
    }
)

login_model = auth_namespace.model(
    'Login',
    {
        'email': fields.String(True, 'User Email'),
        'password': fields.String(True, 'User Password'),
    }
)

register_model = auth_namespace.model(
    'Register',
    {
        'firstName': fields.String(required=True, description='User First Name'),
        'lastName': fields.String(required=True, description='User Last Name'),
        'email': fields.String(required=True, description='User Email'),
        'password': fields.String(required=True, description='User Password'),
        'phone_Number': fields.String(required=True, description='User Phone Number'),
    }
)


@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(register_model)
    @auth_namespace.doc(
        description='Register a new user',
    )
    def post(self):
        """ Register a new user """
        data = auth_namespace.payload
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST
        user = User(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            phone_Number=data['phone_Number'],
        )
        user.save()
        user_response = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_Number': user.phone_Number,
            'user_type': user.user_type
        }
        return user_response, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    @auth_namespace.doc(
        description='Login a user',
    )
    def post(self):
        """ Login a user """
        data = auth_namespace.payload
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if (user is not None) and check_password_hash(user.password_hash, password):
            if user.id is None:
                return {"message": "User ID is None"}, HTTPStatus.INTERNAL_SERVER_ERROR
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK


@auth_namespace.route('/users')
class GetAllUsers(Resource):
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description='Get all users',
    )
    @jwt_required()
    @admin_required
    def get(self):
        """ Get all users """
        users = User.query.all()
        return users, HTTPStatus.OK


# test from here
@auth_namespace.route('/update_user_details')
class UpdateUserDetails(Resource):
    @auth_namespace.expect(register_model)
    @auth_namespace.doc(
        description='Update user details',
    )
    @jwt_required()
    def patch(self):
        """ Update user details """
        data = auth_namespace.payload
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        user.firstName = data['firstName']
        user.lastName = data['lastName']
        user.email = data['email']
        user.password_hash = generate_password_hash(data['password'])
        user.phone_Number = data['phone_Number']
        user.update()
        user_response = {
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'phone_Number': user.phone_Number,
            'user_type': user.user_type
        }
        return user_response, HTTPStatus.OK


@auth_namespace.route('/delete_user/<string:user_id>')
class DeleteUser(Resource):
    @auth_namespace.doc(
        description='Delete user',
    )
    @jwt_required()
    @admin_required
    def delete(self, user_id):
        """ Delete user """
        user = User.query.get_or_404(user_id)
        user.delete()
        return {'message': 'User successfully deleted'}, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
    @auth_namespace.doc(
        description='Logout user',
    )
    @jwt_required()
    def post(self):
        """ Logout user """
        token = get_jwt()
        jti = get_jwt()['jti']
        token_type = token['type']
        BLACKLIST.add(jti)
        return {'message': f"{token_type.capitalize()} token successfully revoked"}, HTTPStatus.OK
