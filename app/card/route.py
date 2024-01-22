
from pymysql import IntegrityError
from app.card.containers import Managers
import json
from datetime import datetime

# Blueprint Configuration
# from . import blueprint
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request
from app.card.models import CardSchema
from app.user.utils import token_required
from werkzeug.exceptions import HTTPException
# Start listening events
object_manager = Managers.object_manager()

blueprint = Blueprint(
    'card',
    __name__,
    url_prefix='/card'
)


@swag_from('swagger/list.yml', methods=['GET'])
@blueprint.route("/list", methods=['GET'])
def _list():
    try:
        result = object_manager.service.list()
        records_serialized = CardSchema(many=True).dump(result)
        objects = {'cards': records_serialized}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@blueprint.route("/_detail_list", methods=['GET'])
def _detail_list():
    try:
        data = {
            'label': request.json['label'],
            'card_no': request.json['card_no']
        }
        services = [result._asdict()
                    for result in object_manager.service.list()]
        objects = {'cards': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@blueprint.route("/update", methods=['GET'])
def _update():
    try:
        data = {
            'id': request.json['id'],
            'label': request.json['label'],
            'card_no': request.json['card_no'],
            'user_id': request.json['user_id'],
            'status': request.json['status'],
        }
        services = object_manager.service.update(data)
        objects = {'cards': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@blueprint.route("/delete", methods=['GET'])
def _delete():
    try:
        data = {
            'card_no': request.json['card_no']
        }
        services = object_manager.service.delete(data)
        objects = {'cards': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@token_required
@swag_from('swagger/create.yml', methods=['POST'])
@blueprint.route("/create", methods=['POST'])
def _create():
    try:
        # time__ = datetime.now()
        # formatted_time = time__.strftime("%Y-%m-%d %H:%M:%S")
        # # data'da eksiklik oldu mu hata fırlat
        # data = {
        #     'label': str(request.json['label']),
        #     'card_no': str(request.json['card_no']),
        #     'user_id': int(request.json['user_id']),
        #     'status': str(request.json['status']),
        #     'date_created': formatted_time,
        #     'date_modified': formatted_time
        # }
        card_schema = CardSchema()
        data = card_schema.load(request.json)
        services = object_manager.service.create(data)
        objects = {'services': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e
