from api.model.transaction import TransactionModel  # noqa
from datetime import datetime
from sql_alchemy import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class SourceModel(db.Model):
    __tablename__ = 'sources'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(12))
    name = db.Column(db.String(50))
    balance = db.Column(db.Integer)
    closing_day = db.Column(db.Integer)
    limit = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)
    transactions = relationship("TransactionModel", backref='source')

    @classmethod
    def find_source_by_id(cls, source_id):
        source = cls.query.filter_by(
            id=source_id,
            is_deleted=False
        ).first()
        if source:
            return source
        return None

    @property
    def update_args(self):
        return ['name', 'balance', 'closing_day', 'limit']

    def json(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'name': self.name,
            'balance': self.balance,
            'closing_day': self.closing_day,
            'limit': self.limit
        }

    def save_source(self):
        db.session.add(self)
        db.session.commit()

    def update_source(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_source(self):
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()