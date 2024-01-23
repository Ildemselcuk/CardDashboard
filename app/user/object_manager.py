import app
import jwt
import random
import logging
from app.user.models import User
from datetime import datetime, timedelta
from app.card.route import object_manager as card_manager
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

    def login(self, data):
        try:
            login_user = self._client.user.login(data)
            secret = app.config.config_dict.get("Debug").SECRET_KEY

            #When the user enters the system, 
            #check the last card that is passive and pull active 
            #if it is on the same date as the date of entry            
            if login_user:
                data_ = {
                    "user_id": login_user.id,
                    "status": "PASSIVE",
                    # "date_created":datetime.today().date()
                }
                card_manager.service.update_card_status(data_)

            token = jwt.encode({
                'email': data.get('email'),
                'user_id': login_user.id,
                # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
                'expiration': str(datetime.utcnow() + timedelta(seconds=300))
            },
                secret, algorithm="HS256")
            
            return token
        except Exception as e:
            self._logger.error(
                f"An error occurred while logining user: {str(e)}")
            raise  # Re-raise the caught exception

    def create(self, data):
        try:
            new_user = self._client.user.create(User(**data))
            if new_user:
                card_data = {
                    'label': ' initial test card with user id '.join(str(new_user)),
                    'card_no': generate_card_number(),
                    'user_id': new_user,
                    'status': 'PASSIVE',
                    'date_created': data.get("date_created", None),
                    'date_modified': data.get("date_created", None)
                }
                card_manager.service.create(card_data)
        except Exception as e:
            self._logger.error(
                f"An error occurred while creating a new user: {str(e)}")
            raise  # Re-raise the caught exception

    def update(self):
        try:
            return self._client.user.update()
        except Exception as e:
            self._logger.error(
                f"An error occurred while updating a user: {str(e)}")
            raise  # Re-raise the caught exception

    def delete(self, data):
        try:
            login_user = self._client.user.login(data)
            if login_user:
                return self._client.user.delete()
            return
        except Exception as e:
            self._logger.error(
                f"An error occurred while deleting a user: {str(e)}")
            raise  # Re-raise the caught exception


def generate_card_number():
    try:
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    except Exception as e:
        self._logger.error(
            f"An error occurred while generating a random card number: {str(e)}")
        raise  # Re-raise the caught exception
