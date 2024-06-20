from ..utils import db
import uuid


def generate_id():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(50), primary_key=True, default=generate_id)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    phone_Number = db.Column(db.String(50), nullable=False)
    order = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete')
    user_type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def __repr__(self):
        return f'<User {self.email}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
