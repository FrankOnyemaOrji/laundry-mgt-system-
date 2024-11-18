import unittest
from unittest.mock import patch
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

    @patch('backend.API.models.users.User.query.get')
    def test_get_all_orders(self, mock_user_query):
        mock_user_query.return_value = True  # Mock user exists

        token = create_access_token(identity="test_user_id")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/order/user/test_user_id/orders", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # @patch('backend.API.models.users.User.query.filter_by')
    # def test_create_order(self, mock_user_query):
    #     mock_user_query.return_value.first.return_value = True  # Mock user exists
    #
    #     data = {
    #         "order_status": "PENDING",
    #         "order_details": "Order Details",
    #         "order_address": "Order Address",
    #         "quantity": 2
    #     }
    #     token = create_access_token(identity="test_user_id")
    #
    #     headers = {
    #         "Authorization": f"Bearer {token}"
    #     }
    #
    #     # Corrected route URL
    #     response = self.client.post("/order/order/create_order", json=data, headers=headers)
    #
    #     self.assertEqual(response.status_code, 201)
    #     orders = Order.query.all()
    #     order_id = orders[0].id
    #     self.assertEqual(len(orders), 1)
    #     self.assertEqual(response.json["id"], order_id)
    #     self.assertEqual(response.json["order_status"], "PENDING")
    #     self.assertEqual(response.json["order_details"], "Order Details")
    #     self.assertEqual(response.json["order_address"], "Order Address")
    #     self.assertEqual(response.json["quantity"], 2)

