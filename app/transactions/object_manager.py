import logging
from app.transactions.models import Transactions


#
# Object manager is the core component of the master module. Object manager listens for container events and stores them
# to a structure. (Docker swarm manager can access services trough native api but can not gather information about the
# containers that are running on the other nodes. This structure saves container information from captured containers
# events). Object manager also controls all execution operations.
#

class ObjectManager:

    def __init__(self, client):
        # Get logger
        self._logger = logging.getLogger(self.__class__.__name__)
        # Set logging level to logging.DEBUG if you want to debug object manager
        self._logger.setLevel(logging.ERROR)

        # Extended docker client
        self._client = client

    # Service operation manager
    @property
    def service(self):
        return ServiceManager(client=self._client, logger=self._logger)


class ServiceManager:
    """
    Object manager uses this class as a property.
    All service operations executed by docker client is responsibility of the service manager.
    """

    def __init__(self, client, logger):
        self._client = client
        self._logger = logger

   

    def report(self):
        return self._client.transactions.report()
    
    def list(self):
        filter_ = {
            Transactions.status.notin_("DELETED"),
            or_(Card.label.like(func.concat('%', data.get("label", None), '%')),
                Card.card_no.like(func.concat('%', data.get("card_no", None), '%')))
        }
        return self._client.transactions.list()
    
    
    

    def create(self, data):
        self._client.transactions.create(Transactions(**data))

    def update(self):
        return self._client.transactions.update()

    def delete(self):
        return self._client.transactions.delete()
