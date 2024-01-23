# import logging

# from sqlalchemy import and_, or_, func
# from app.card.models import Card
# from app.transactions.models import Transactions
# from datetime import datetime, timedelta


# #
# # Object manager is the core component of the master module. Object manager listens for container events and stores them
# # to a structure. (Docker swarm manager can access services trough native api but can not gather information about the
# # containers that are running on the other nodes. This structure saves container information from captured containers
# # events). Object manager also controls all execution operations.
# #

# class ObjectManager:

#     def __init__(self, client):
#         # Get logger
#         self._logger = logging.getLogger(self.__class__.__name__)
#         # Set logging level to logging.DEBUG if you want to debug object manager
#         self._logger.setLevel(logging.ERROR)

#         # Extended docker client
#         self._client = client

#     # Service operation manager
#     @property
#     def service(self):
#         return ServiceManager(client=self._client, logger=self._logger)


# class ServiceManager:
#     """
#     Object manager uses this class as a property.
#     All service operations executed by docker client is responsibility of the service manager.
#     """

#     def __init__(self, client, logger):
#         self._client = client
#         self._logger = logger

#     def get(self):
#         return self._client.card.get()

#     def detail_list(self, data):
#         # gunceleme tarhine göre listele
#         # filter_ = {
#         #     Card.status.notin_("DELETED"),
#         #     or_(Card.label.like(func.concat('%', data.get("label", None), '%')),
#         #         Card.card_no.like(func.concat('%', data.get("card_no", None), '%')))
#         # }
#         return self._client.card.detail_list(data)

#     # def list(self):
#     #     # gunceleme tarhine göre listele
#     #     # filter_ = [
#     #     #     Card.status.notin_(["DELETED"])
#     #     # ]
#     #     # order_by = [
#     #     #     Card.date_modified.desc()
#     #     # ]
#     #     # return self._client.card.list(filters=filter_, order_by=order_by)
#     #     return self._client.card.list()

#     def update_card_status(self, data):
#         return self._client.card.update(data)

#     def create(self, data):
#         self._client.card.create(Card(**data))

#     def update(self, data):

#         return self._client.card.update(data)


#     def delete(self, data):
#         # kullanıcı aktif kartlarını listele 1 den fazla ise gleni sil yok ise 1 den az ise silme hata er aktif bir kartınız bulunmaktadır.
#         # kullanıcı  silme işlmeini ypacagı kart ve en az bir kart aktif olmalı
#         # kullanıcının kartı silinmis ise bu kart zaten silinmiş diye uyarı verilmelidir.
#         return self._client.card.delete(data)
#         # exception fırlat 1 den az kayıt var diye


import logging
from sqlalchemy import and_, or_, func
from app.card.models import Card
from app.transactions.models import Transactions
from datetime import datetime, timedelta


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
                f"An error occurred while getting detailed list: {str(e)}")
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

    def update(self, data):
        try:
            return self._client.card.update(data)
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
