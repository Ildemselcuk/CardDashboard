from app import db, ma
from marshmallow import fields, ValidationError, validates
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(100))
    date_created = db.Column(
        db.DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_modified = db.Column(db.DateTime, default=datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"), onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', '')
        self.password = kwargs.get('password', '')
        self.date_created = kwargs.get('date_created')
        self.date_modified = kwargs.get('date_modified')

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


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Specify the model for SQLAlchemyAutoSchema
        model = User

    # Custom validation to check the validity of the email
    @validates('email')
    def validate_email(self, value):
        # Check if the email is already associated with a user
        user_with_email = User.query.filter_by(email=value).first()
        if user_with_email:
            # Raise a validation error if the email is already in use
            raise ValidationError('This email address is already in use.')


class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Specify the model for SQLAlchemyAutoSchema
        model = User
        # include only the 'email', 'password' field
        fields = ('email', 'password',)
