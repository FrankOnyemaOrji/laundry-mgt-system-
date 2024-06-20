import unittest
from backend.API.config.config import config_dict
from backend.API.utils import db
from backend.API import create_app
from backend.API.models.order import Order
from flask_jwt_extended import create_access_token


class TestOrder(unittest.TestCase):
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

    def test_get_all_orders(self):
        token = create_access_token(identity="test_user_first_name")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/order", headers=headers)
        assert response.status_code == 200
        assert response.json == []

    def test_create_order(self):
        data = {
            "order_status": "PENDING",
            "order_details": "Order Details",
            "order_address": "Order Address",
            "quantity": 2
        }
        token = create_access_token(identity="test_user_first_name")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/order/create_order", json=data, headers=headers)
        assert response.status_code == 201
        orders = Order.query.all()
        order_id = orders[0].id
        assert len(orders) == 1
        assert response.json["id"] == order_id
        assert response.json["order_status"] == "PENDING"
        assert response.json["order_details"] == "Order Details"
        assert response.json["order_address"] == "Order Address"
        assert response.json["quantity"] == 2
