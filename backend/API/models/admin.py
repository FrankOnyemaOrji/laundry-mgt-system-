from ..utils import db
from .users import User


class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.String(50), db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
