# -*- encoding: utf-8 -*-


import datetime
from app import db, ma
from app.card.models import Card
from marshmallow import fields
from datetime import datetime


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(256))
    description = db.Column(db.String(256))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_modified = db.Column(db.DateTime, default=datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"), onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __init__(self, amount, description, card_id, date_created=None, date_modified=None):
        self.amount = amount
        self.description = description
        self.card_id = card_id
        self.date_created = date_created
        self.date_modified = date_modified

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for field_name, value in kwargs.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, test_id):
        return cls.query.get(test_id)

    @classmethod
    def list_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_params(cls, params):
        query = cls.query

        for key, value in params.items():
            column = getattr(cls, key, None)
            if column is not None:
                query = query.filter(column == value)

        return query.all()

    @classmethod
    def count(cls):
        return cls.query.count()


class TransactionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transactions
