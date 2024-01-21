from sqlalchemy import or_, and_

from app import db


class Database:
    def __init__(self):
        self._db = db

    def get(self, model, id):
        try:
            return self._db.session.query(model).get(id)
        except Exception as err:
            raise err

    def get_records(self, model, columns, filter_=None, or_operator=None, and_operator=None, **kwargs):
        """
        model = database model object (model of table)
        columns =
        filter =
        kwargs =
        """

        try:
            ## todo: think about marshmallow
            if filter_:
                result = []
                if or_operator:
                    result_query = self._db.session.query(model).with_entities(*columns).filter(or_(*filter_)).all()


                elif and_operator:
                    result_query = self._db.session.query(model).with_entities(*columns).filter(and_(*filter_)).all()

                for row in result_query:
                    result.append(row._asdict())

                return result
            else:
                return self._db.session.query(model).with_entities(*columns).filter_by(**kwargs).all()

        except Exception as err:
            raise err

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

    def get_or_create(self, model, **kwargs):
        try:
            instance = self._db.session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                self._db.session.add(instance)
                self.commit()
                return instance
        except Exception as err:
            raise err

    def create(self, data):
        try:
            self._db.session.add(data)
            self.commit()
            return data.id
        except Exception as err:
            raise err

    def remove_db_record(self, model, delete_column, new_record_ids, db_ids):

        try:
            remove_list = list(set(db_ids) - set(new_record_ids))
            for id in remove_list:
                self._db.session.query(model).filter(delete_column == id).delete()
            self.commit()
        except Exception as err:
            raise err

    def delete(self, model, id):

        try:
            self._db.session.query(model).filter_by(id=id).delete()
            self.commit()
        except Exception as err:
            raise err

    def commit(self):
        from sqlalchemy.exc import SQLAlchemyError
        try:
            self._db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
