import unittest
from unittest.mock import patch
from backend.API.config.config import config_dict
from backend.API.utils import db
from backend.API import create_app


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appctx.pop()
        self.client = None
        self.app = None

    @patch('backend.API.models.users.User')
    def test_user_registration(self, mock_user):
        mock_user.return_value = True  # Mock user creation

        data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "testuser@example.com",
            "password": "password123",
            "phone_Number": "1234567890"
        }
        response = self.client.post("/auth/register", json=data)
        print(response.status_code)
        print(response.json)
        assert response.status_code == 201

    @patch('backend.API.models.users.User')
    def test_user_login(self, mock_user):
        mock_user.return_value = True  # Mock user login

        data = {
            "email": "testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post("/auth/login", json=data)
        assert response.status_code == 200
