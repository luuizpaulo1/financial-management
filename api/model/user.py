from api.model.transaction import TransactionModel  # noqa
from api.model.source import SourceModel  # noqa
from datetime import datetime
from sql_alchemy import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(255))
    document = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    is_deleted = db.Column(db.Boolean, default=False)
    transactions = relationship("TransactionModel", backref='owner')
    sources = relationship("SourceModel", backref='owner')

    @classmethod
    def find_user_by_id(cls, user_id):
        user = cls.query.filter_by(
            id=user_id,
            is_deleted=False
        ).first()
        if user:
            return user
        return list()

    @classmethod
    def find_user_by_document(cls, document):
        users = cls.query.filter_by(
            document=document,
            is_deleted=False
        ).all()
        if users:
            return users
        return list()

    @property
    def update_args(self):
        return ['name', 'document', 'birth_date']

    def json(self):
        return {
            'id': str(self.id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'name': self.name,
            'document': self.document,
            'birth_date': str(self.birth_date)
        }

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()