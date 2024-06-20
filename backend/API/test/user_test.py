import unittest
from ..config.config import config_dict
from ..utils import db
from .. import create_app
from ..models.users import User


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

    def test_user_registration(self):
        data = {
            "first_name": "test_user_first_name",
            # "last_name": "test_user_last_name",
            "email": "testuser@gmail.com",
            "password": "test_password"
        }
        response = self.client.post("/auth/register", json=data)
        user = User.query.filter_by(email="testuser@gmail.com").first()

        assert user.first_name == "test_user_first_name"
        # assert user.last_name == "test_user_last_name"
        assert response.status_code == 201

    def test_user_login(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post("/auth/login", json=data)
        assert response.status_code == 200


