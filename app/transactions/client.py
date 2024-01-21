import json
import logging
from app.card.models import Card
from app.transactions.models import Transactions
from sqlalchemy import or_, func, case

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
            return self._db.session.query(self.__model).with_entities(*columns).filter_by(**filters).all()
        except Exception as err:
            raise err

    def report(self):
        try:
            result = (
                db.session.query(
                    func.count(
                        case((Card.status == 'ACTIVE', Card.id), else_=None)
                    ).label('active_card_count'),
                    func.sum(
                        case((Card.status == 'ACTIVE', Transactions.amount), else_=0)
                    ).label('active_card_spending'),
                    func.count(
                        case((Card.status == 'PASSIVE', Card.id), else_=None)
                    ).label('passive_card_count'),
                    func.sum(
                        case(
                            (Card.status == 'PASSIVE', Transactions.amount), else_=0)
                    ).label('passive_card_spending')
                )
                .join(Transactions, Transactions.card_id == Card.id)
                .group_by()
                .one()
            )
            # Dict objesi oluşturma
            result_dict = {
                'active_card_count': result.active_card_count,
                'active_card_spending': result.active_card_spending,
                'passive_card_count': result.passive_card_count,
                'passive_card_spending': result.passive_card_spending
            }
            return result_dict
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
