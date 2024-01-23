import logging
from app.card.models import Card


class ObjectManager:

    def __init__(self, client):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.ERROR)
        self._client = client

    @property
    def service(self):
        return ServiceManager(client=self._client, logger=self._logger)


class ServiceManager:

    def __init__(self, client, logger):
        self._client = client
        self._logger = logger

    def get(self):
        try:
            return self._client.card.get()
        except Exception as e:
            self._logger.error(
                f"An error occurred while getting data: {str(e)}")
            raise  # Re-raise the caught exception

    def list(self):
        try:
            return self._client.card.list()
        except Exception as e:
            self._logger.error(
                f"An error occurred while getting list: {str(e)}")
            raise  # Re-raise the caught exception

    def detail_list(self, data):
        try:
            return self._client.card.detail_list(data)
        except Exception as e:
            self._logger.error(
                f"An error occurred while getting detailed list: {str(e)}")
            raise  # Re-raise the caught exception

    def update_card_status(self, data):
        try:
            return self._client.card.update_card_status(data)
        except Exception as e:
            self._logger.error(
                f"An error occurred while updating card status: {str(e)}")
            raise  # Re-raise the caught exception

    def create(self, data):
        try:
            self._client.card.create(Card(**data))
        except Exception as e:
            self._logger.error(
                f"An error occurred while creating a new card: {str(e)}")
            raise  # Re-raise the caught exception

    def update(self, data, current):
        try:
            _instance = self._client.card.one(current)
            if _instance:
                self._client.card.update(_instance, data)
                return True
            return False
        except Exception as e:
            self._logger.error(
                f"An error occurred while updating card information: {str(e)}")
            raise  # Re-raise the caught exception

    def delete(self, data):
        try:
            return self._client.card.delete(data)
        except Exception as e:
            self._logger.error(
                f"An error occurred while deleting a card: {str(e)}")
            raise  # Re-raise the caught exception
