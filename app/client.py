import json
import logging
from app.card.models import Card
from app.transactions.models import Transactions
from app.user.models import User
from sqlalchemy import or_, and_, func, case
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, timedelta
import pymysql.err
from . import db


class Client:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.ERROR)

    @property
    def card(self):
        return CardDbService(client=self)

    @property
    def transactions(self):
        return TransactionDbService(client=self)

    @property
    def user(self):
        return UserDbService(client=self)


class _BaseDbService:
    def __init__(self, client, model=None):
        self._client = client
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.ERROR)
        self._db = db
        self.model = model

    def get(self, filters={}, order_by={Card.date_modified.desc()}):
        try:
            return self._db.session.query(self.model).filter(*filters).order_by(*order_by).one()
        except NoResultFound as no_result_err:
            self.logger.error("No result found!")
            raise no_result_err  # Re-raise the NoResultFound exception
        except MultipleResultsFound as multiple_results_err:
            self.logger.error("Multiple results found!")
            raise multiple_results_err  # Re-raise the MultipleResultsFound exception
        except Exception as err:
            self.logger.error(
                f"An error occurred while getting a record: {str(err)}")
            raise err  # Re-raise the general exception

    def list(self, filters=[], order_by=[]):
        try:
            return self._db.session.query(self.model).filter(
                *filters).order_by(*order_by).all()
        except Exception as err:
            self.logger.error(
                f"An error occurred while getting a list of records: {str(err)}")
            raise err  # Re-raise the exception

    def count(self, columns=[], filters={}):
        try:
            return self._db.session.query(self.model).with_entities(*columns).filter_by(**filters).count()
        except Exception as err:
            self.logger.error(
                f"An error occurred while counting records: {str(err)}")
            raise err  # Re-raise the exception

    def create(self, data):
        try:
            self._db.session.add(data)
            self.commit()
            return data.id
        except IntegrityError as integrity_err:
            self.logger.error("Duplicate entry detected!")
            self._db.session.rollback()
            raise integrity_err  # Re-raise the IntegrityError
        except pymysql.err.Error as mysql_err:
            self.logger.error(f"MySQL error occurred: {str(mysql_err)}")
            self._db.session.rollback()
            raise mysql_err  # Re-raise the MySQL-specific error
        except SQLAlchemyError as err:
            self.logger.error(
                f"An error occurred while creating a record: {str(err)}")
            self._db.session.rollback()
            raise err  # Re-raise the general SQLAlchemyError

    def update(self, row, column, value):
        try:
            setattr(row, column, value)
            self.commit()
        except AttributeError as attribute_err:
            self.logger.error(
                f"Attribute error occurred: {str(attribute_err)}")
            self._db.session.rollback()
            raise attribute_err  # Re-raise the AttributeError
        except IntegrityError as integrity_err:
            self.logger.error("Duplicate entry detected!")
            self._db.session.rollback()
            raise integrity_err  # Re-raise the IntegrityError
        except pymysql.err.Error as mysql_err:
            self.logger.error(f"MySQL error occurred: {str(mysql_err)}")
            self._db.session.rollback()
            raise mysql_err  # Re-raise the MySQL-specific error
        except SQLAlchemyError as err:
            self.logger.error(
                f"An error occurred while updating a record: {str(err)}")
            self._db.session.rollback()
            raise err  # Re-raise the general SQLAlchemyError

    def delete(self, data):
        try:
            instance__ = self._db.session.query(
                self.model).filter_by(**data).one()
            instance__.status == "DELETED"
            self.commit()
        except NoResultFound as no_result_err:
            self.logger.error("No result found!")
            raise no_result_err  # Re-raise the NoResultFound exception
        except MultipleResultsFound as multiple_results_err:
            self.logger.error("Multiple results found!")
            raise multiple_results_err  # Re-raise the MultipleResultsFound exception
        except Exception as err:
            self.logger.error(
                f"An error occurred while deleting a record: {str(err)}")
            raise err  # Re-raise the general exception

    def commit(self):
        try:
            self._db.session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"An error occurred during commit: {str(e)}")
            self._db.session.rollback()
            raise e  # Re-raise the exception


class CardDbService(_BaseDbService):
    def __init__(self, client):
        super().__init__(client, model=Card)
        self.model = Card

    def count(self, columns=[], filters={}):
        try:
            return self._db.session.query(self.model).with_entities(*columns).filter_by(**filters).count()
        except Exception as err:
            self.logger.error(
                f"An error occurred while counting card records: {str(err)}")
            raise err  # Re-raise the exception

    def detail_list(self, data, filters=[], order_by=[]):
        try:
            filters = {
                Card.status.notin_("DELETED"),
                or_(Card.label.like(func.concat('%', data.get("label", None), '%')),
                    Card.card_no.like(func.concat('%', data.get("card_no", None), '%')))
            }
            order_by = [
                Card.date_modified.desc()
            ]
            r_ = super().filter_by_params(params=filters)
            # r_ = self.model.filter_by_params(params=filters)
            return r_
        except Exception as err:
            self.logger.error(
                f"An error occurred while getting detailed card list: {str(err)}")
            raise err  # Re-raise the exception

    def list(self, filters=[], order_by=[]):
        try:
            filters = [
                Card.status.notin_(["DELETED"])
            ]
            order_by = [
                Card.date_modified.desc()
            ]
            r_ = self.model.filter_by_params(params=filters, order_by=order_by)
            return r_
        except Exception as err:
            self.logger.error(
                f"An error occurred while getting card list: {str(err)}")
            raise err  # Re-raise the exception

    def update_card_status(self, data):
        cond_ = [
            and_(Card.status == data.get("status", None),
                 Card.user_id == data.get("user_id", None))
        ]
        card_data = self._client.card.get(filters=cond_)
        if card_data is not None:
            time__ = datetime.now()
            formatted_time = time__.strftime("%Y-%m-%d %H:%M:%S")
            card_data.status = "ACTIVE"
            card_data.date_modified = formatted_time
            self._client.card.commit()

    def delete(self, data):
        try:
            filter_ = {
                Card.status.in_("ACTIVE")
            }
            order_by = [
                Card.date_modified.desc()
            ]
            cards = super().count(params=filter_, order_by=order_by)
            cards = self.count(filters=filter_)
            if cards > 1:

                instance__ = self._db.session.query(
                    self.model).filter_by(**data).one()
                instance__.status == "DELETED"
                self.commit()
                return instance__
            return
        except Exception as err:
            self.logger.error(
                f"An error occurred while deleting card: {str(err)}")
            raise err  # Re-raise the exception

    def update(self, data):
        try:
            cond_ = [
                Card.id == data.get("id", None),
            ]

            time__ = datetime.now()
            formatted_time = time__.strftime("%Y-%m-%d %H:%M:%S")
            card_data = super().get(filters=cond_)
            del data["id"]
            for key, value in data.items():
                setattr(card_data, key, value)
            setattr(card_data, Card.date_modified, formatted_time)
            self.commit()
        except Exception as err:
            self.logger.error(
                f"An error occurred while updating card: {str(err)}")
            raise err  # Re-raise the exception


class TransactionDbService(_BaseDbService):
    def __init__(self, client):
        super().__init__(client, model=Transactions)
        self.model = Transactions

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
            result_dict = {
                'active_card_count': result.active_card_count,
                'active_card_spending': result.active_card_spending,
                'passive_card_count': result.passive_card_count,
                'passive_card_spending': result.passive_card_spending
            }
            return result_dict
        except Exception as err:
            self.logger.error(
                f"An error occurred while generating a report: {str(err)}")
            raise err  # Re-raise the exception


class UserDbService(_BaseDbService):
    def __init__(self, client):
        super().__init__(client, model=User)
        self.model = User

    def login(self, data):
        try:
            return self._db.session.query(self.model).filter(and_(self.model.email == data.get("email", None), self.model.password == data.get("password", None))).one()
        except Exception as err:
            self.logger.error(
                f"An error occurred while logging in: {str(err)}")
            raise err  # Re-raise the exception
