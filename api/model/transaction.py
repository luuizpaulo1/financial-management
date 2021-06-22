from sql_alchemy import db
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'))
    source_id = db.Column(UUID(as_uuid=True), ForeignKey('sources.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    subcategory = db.Column(db.String(50))
    description = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    installments = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def find_transaction_by_id(cls, transaction_id):
        transaction = cls.query.filter_by(
            id=transaction_id,
            is_deleted=False
        ).first()
        if transaction:
            return transaction
        return None

    @property
    def update_args(self):
        return ['source_id', 'category', 'subcategory', 'description', 'amount', 'installments']

    def json(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'category': self.category,
            'subcategory': self.subcategory,
            'description': self.description,
            'amount': self.amount,
            'installments': self.installments
        }

    def save_transaction(self):
        self.source.balance -= self.amount
        db.session.add(self)
        db.session.commit()

    def update_transaction(self, **kwargs):
        amount = kwargs.get('amount')
        if amount:
            self.source.balance -= amount - self.amount

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_transaction(self):
        self.source.balance += self.amount
        self.is_deleted = True
        db.session.add(self)
        db.session.commit()
