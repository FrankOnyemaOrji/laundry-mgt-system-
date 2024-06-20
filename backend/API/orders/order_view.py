from flask_restx import Namespace, Resource, fields
from ..models.order import Order
from ..models.users import User
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

order_namespace = Namespace("order", description="Order related operations")

order_model = order_namespace.model(
    "Order",
    {
        "id": fields.String(required=True, description="Order ID"),
        "order_status": fields.String(required=True, description="Order Status",
                                      enum=["PENDING", "CONFIRMED", "CANCELLED", "IN_PROGRESS", "COMPLETED",
                                            "DELIVERED"]),
        "order_details": fields.String(required=True, description="Order Total"),
        "order_address": fields.String(required=True, description="Order Address"),
        "quantity": fields.Integer(required=True, description="Order Quantity"),
    },
)

order_status_model = order_namespace.model(
    'OrderStatus', {
        'order_status': fields.String(description='Current Order Status', required=True,
                                      enum=["PENDING", "CONFIRMED", "CANCELLED", "IN_PROGRESS", "COMPLETED",
                                            "DELIVERED"])
    }
)

create_order_model = order_namespace.model(
    'CreateOrder', {
        'order_status': fields.String(description='Order Status', required=True,
                                      enum=["PENDING", "CONFIRMED", "CANCELLED", "IN_PROGRESS", "COMPLETED",
                                            "DELIVERED"]),
        'order_details': fields.String(description='Order Details', required=True),
        'order_address': fields.String(description='Order Address', required=True),
        'quantity': fields.Integer(description='Order Quantity', required=True)
    }
)


@order_namespace.route("/create_order")
class CreateOrder(Resource):
    @order_namespace.expect(create_order_model)
    @order_namespace.doc(description="Create a new order")
    @jwt_required()
    def post(self):
        """ Create a new order """
        data = order_namespace.payload
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        new_order = Order(
            order_status=data['order_status'],
            order_details=data['order_details'],
            order_address=data['order_address'],
            quantity=data['quantity'],
        )
        new_order.user = user  # Assign the User object to the user field
        new_order.save()
        order_response = {
            'id': new_order.id,
            'order_status': str(new_order.order_status),  # Convert order_status to a string
            'order_details': new_order.order_details,
            'order_address': new_order.order_address,
            'quantity': new_order.quantity,
        }
        return order_response, HTTPStatus.CREATED


@order_namespace.route("/order/<string:order_id>")
class UpdateOrder(Resource):
    @order_namespace.expect(create_order_model)
    @order_namespace.doc(
        description="Update order details",
        params={'order_id': 'Order ID'}
    )
    @jwt_required()
    def patch(self, order_id):
        """ Update order details """
        data = order_namespace.payload
        order = Order.get_by_id(order_id)
        order.order_status = data['order_status']
        order.order_details = data['order_details']
        order.order_address = data['order_address']
        order.quantity = data['quantity']
        order.update()
        order_response = {
            'id': order.id,
            'order_status': str(order.order_status),
            'order_details': order.order_details,
            'order_address': order.order_address,
            'quantity': order.quantity,
        }
        return order_response, HTTPStatus.OK


@order_namespace.route("/order/<string:order_id>")
class DeleteOrder(Resource):
    @order_namespace.doc(
        description="Delete an order",
        params={'order_id': 'Order ID'}
    )
    @jwt_required()
    def delete(self, order_id):
        """ Delete an order """
        order = Order.get_by_id(order_id)
        order.delete()
        return {"message": "Order deleted successfully"}, HTTPStatus.OK


@order_namespace.route("/user/<string:user_id>/orders/<string:order_id>")
class GetSpecificOrder(Resource):
    @order_namespace.doc(
        description="Get a specific order",
        params={'user_id': 'User ID', 'order_id': 'Order ID'}
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """ Get a specific order """
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
        order_response = {
            'id': order.id,
            'order_status': str(order.order_status),
            'order_details': order.order_details,
            'order_address': order.order_address,
            'quantity': order.quantity,
        }
        return order_response, HTTPStatus.OK


@order_namespace.route("/user/<string:user_id>/orders")
class GetOrders(Resource):
    @order_namespace.doc(
        description="Get all orders",
        params={'user_id': 'User ID'}
    )
    @jwt_required()
    def get(self, user_id):
        """ Get all orders """
        orders = Order.query.filter_by(user_id=user_id).all()
        order_response = []
        for order in orders:
            order_response.append({
                'id': order.id,
                'order_status': str(order.order_status),
                'order_details': order.order_details,
                'order_address': order.order_address,
                'quantity': order.quantity,
            })
        return order_response, HTTPStatus.OK


@order_namespace.route("/order/status/<string:order_id>")
class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_status_model)
    @order_namespace.doc(
        description="Update order status",
        params={'order_id': 'Order ID'}
    )
    @jwt_required()
    def patch(self, order_id):
        """ Update order status """
        data = order_namespace.payload
        order = Order.get_by_id(order_id)
        order.order_status = data['order_status']
        order.update()
        order_response = {
            'id': order.id,
            'order_status': str(order.order_status),
            'order_details': order.order_details,
            'order_address': order.order_address,
            'quantity': order.quantity,
        }
        return order_response, HTTPStatus.OK
