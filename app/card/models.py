from app import db, ma
from app.user.models import User
from sqlalchemy import UniqueConstraint

class baseModel(db.Model):
    def __init__(self, **kwargs):
        pass

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
    def list_all(cls, order_by):

        return cls.query.order_by(*order_by).all()

    @classmethod
    def filter_by_params(cls, params, order_by):
        query = cls.query

        for key, value in params.items():
            column = getattr(cls, key, None)
            if column is not None:
                query = query.filter(column == value)

        return query.order_by(*order_by).all()

    @classmethod
    def count(cls):
        return cls.query.count()

    
class Card(baseModel):
    __tablename__ = 'card'
   
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256))
    card_no = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(256))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    __table_args__ = (UniqueConstraint(
        'user_id', 'card_no', name='_user_card_uc'),)

    def __init__(self, label, card_no, user_id, status, date_created=None, date_modified=None):
        self.label = label
        self.card_no = card_no
        self.user_id = user_id
        self.status = status
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
    def list_all(cls, order_by):

        return cls.query.order_by(*order_by).all()

    @classmethod
    def filter_by_params(cls, params, order_by):
        query = cls.query

        for key, value in params.items():
            column = getattr(cls, key, None)
            if column is not None:
                query = query.filter(column == value)

        return query.order_by(*order_by).all()
    
    @classmethod
    def filter_by_params_one(cls, params, order_by):
        query = cls.query

        for key, value in params.items():
            column = getattr(cls, key, None)
            if column is not None:
                query = query.filter(column == value)

        return query.order_by(*order_by).one()

    @classmethod
    def count(cls, params, order_by):
        query = cls.query

        for key, value in params.items():
            column = getattr(cls, key, None)
            if column is not None:
                query = query.filter(column == value)

        return query.order_by(*order_by).count()


class CardExt(baseModel):
    __tablename__ = 'cardt'
   
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256))
    card_no = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(256))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

class CardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Card

