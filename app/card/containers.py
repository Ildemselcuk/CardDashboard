from dependency_injector import providers, containers

from app.client import Client
from app.card.object_manager import ObjectManager
#
# Dependency injection classes
#

class Clients(containers.DeclarativeContainer):
    client = providers.Singleton(Client)


class Managers(containers.DeclarativeContainer):
    object_manager = providers.Singleton(ObjectManager, Clients.client)
