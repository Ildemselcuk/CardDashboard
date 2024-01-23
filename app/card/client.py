import json
import logging
from app.card.models import Card
from app import db
from sqlalchemy.exc import SQLAlchemyError
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

    def __init__(self,model=None):
        # Get logger
        self.logger = logging.getLogger(self.__class__.__name__)
        # Set logging level to logging.DEBUG if you want to debug client
        self.logger.setLevel(logging.ERROR)
        self.model = model

    # Service operations

    @property
    def service(self):
        return DbService(client=self,model=self.model)


class DbService:
    def __init__(self, client,model=None):
        self._client = client
        self.logger = logging.getLogger(self.__class__.__name__)
        # Set logging level to logging.DEBUG if you want to debug client
        self.logger.setLevel(logging.ERROR)
        self._db = db
        self.__model = Card

    # Returns parsed service object
    # NOTE: Simple version of service object does not has nodes and containers

    def get(self, id):
        try:
            return self._db.session.query(self.__model).get(id)
        except Exception as err:
            raise err

    # Returns list of all service objects
    def list(self, columns=[], filters={}):
        try:
            r_ = self._db.session.query(self.__model).filter(*filters).order_by(Card.date_modified.desc()).all()
            return r_
        except Exception as err:
            raise err
    
    # Returns list of all service objects
    def count(self, columns=[], filters={}):
        try:
            return self._db.session.query(self.__model).with_entities(*columns).filter_by(**filters).count()
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

    def delete(self, data):
        try:
            instance__ = self._db.session.query(self.__model).filter_by(**data).one()
            instance__.status == "DELETED"

            self.commit()
        except Exception as err:
            raise err
        
    def commit(self):
        try:
            self._db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
