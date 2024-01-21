import json
import logging
from app.card.models import Card
from app.user.models import User
from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
#
# Docker client implementation with extended methods.
# This class uses both docker python api and docker cli (command line interface) operations.
#  * You need to give docker socket access to this class if you want to run inside docker container
# NOTE: list methods in this class is designed to extract all the information where it is possible. This methods are
# exposed trough api and they are not used for daemon tasks. Performance is not the criteria for this methods.
#
# CAUTION: Docker python SDK uses full ids for the docker objects. On the other hand docker cli only uses short
# version of the object ids (12 character). Full ids are used for the ensure completeness.
#


class Client:

    def __init__(self):
        # Get logger
        self.logger = logging.getLogger(self.__class__.__name__)
        # Set logging level to logging.DEBUG if you want to debug client
        self.logger.setLevel(logging.ERROR)

    # Service operations

    @property
    def service(self):
        return DbService(client=self)


class DbService:
    def __init__(self, client):
        self._client = client
        self.logger = logging.getLogger(self.__class__.__name__)
        # Set logging level to logging.DEBUG if you want to debug client
        self.logger.setLevel(logging.ERROR)
        self._db = db
        self.__model = User

    # Returns parsed service object
    # NOTE: Simple version of service object does not has nodes and containers

    def login(self, data):
        try:
            return self._db.session.query(self.__model).filter(and_(self.__model.email == data.get("email",None),self.__model.password == data.get("password",None))).one()
        except Exception as err:
            raise err

    # Returns list of all service objects
    def list(self, columns=[], filters={}):
        try:
            return self._db.session.query(self.__model).with_entities(*columns).filter_by(Card.user_id == 3,Card.status=="PASSIVE").all()
        except Exception as err:
            raise err

    # Creates a new service with given parameters
    def create(self, data):
        try:
            self._db.session.add(data)
            self.commit()
        except Exception as err:
            raise err

    # Changes service replica count
    def update(self, row, column, value):
        """
        row = row object (db row)
        column = which column
        value = new value
        """

        try:
            setattr(row, column, value)
            self.commit()
        except Exception as err:
            raise err

    def delete(self, id):
        try:
            self._db.session.query(self.__model).filter_by(id=id).delete()
            self.commit()
        except Exception as err:
            raise err
        
    def commit(self):
        try:
            self._db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
