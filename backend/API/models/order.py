from ..utils import db
from enum import Enum
from datetime import datetime
import uuid


class OrderStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    DELIVERED = 'delivered'


def generate_id():
    return str(uuid.uuid4())


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(50), primary_key=True, default=generate_id)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_details = db.Column(db.String(100), nullable=False)
    order_address = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer(), default=1)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Order {self.id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
