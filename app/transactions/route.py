import json
from app.transactions.containers import Managers
from datetime import datetime
from flask import Blueprint, request
from flasgger.utils import swag_from

# Start listening events
object_manager = Managers.object_manager()

blueprint = Blueprint(
    'transaction',
    __name__,
    url_prefix='/transaction'
)

@swag_from('swagger/list.yml', methods=['GET'])
@blueprint.route("/list", methods=['GET'])
def _list():
    try:
        return json.dumps(object_manager.service.report(), indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e

@blueprint.route("/delete", methods=['GET'])
def _delete():
    try:
        data = {
            'card_id': request.json['card_no']
        }
        services = object_manager.service.delete(data)
        objects = {'cards': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e

@swag_from('swagger/create.yml', methods=['POST'])
@blueprint.route("/create", methods=['POST'])
def create():
    try:
        time__ = datetime.now()
        formatted_time = time__.strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'amount': request.json['amount'],
            'card_id': request.json['card_id'],
            'description': request.json['description'],
            'date_created': formatted_time,
            'date_modified': formatted_time
        }
        services = object_manager.service.create(data)
        objects = {'services': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e