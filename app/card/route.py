
import json
from datetime import datetime
from pymysql import IntegrityError
from app.card.containers import Managers
from flasgger.utils import swag_from
from flask import Blueprint, request
from app.card.models import CardSchema, DeleteCardSchema, DetailListCardSchema
from app.user.utils import token_required

# initialize object manager
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
        _serialized = CardSchema(many=True).dump(result)
        objects = {'cards': _serialized}
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
        _schema = DetailListCardSchema()
        data = _schema.load(request.json)
        cards = [result._asdict()
                    for result in object_manager.service.list()]
        objects = {'cards': cards}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@blueprint.route("/update", methods=['GET'])
def _update():
    try:
        # data = {
        #     'id': request.json['id'],
        #     'label': request.json['label'],
        #     'card_no': request.json['card_no'],
        #     'user_id': request.json['user_id'],
        #     'status': request.json['status'],
        # }
        card_schema = CardSchema()
        data = card_schema.load(request.json)
        services = object_manager.service.update(data)
        objects = {'cards': services}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@blueprint.route("/delete", methods=['GET'])
def _delete():
    try:
        # data = {
        #     'card_no': request.json['card_no']
        # }
        _schema = DeleteCardSchema()
        data = _schema.load(request.json)
        res = object_manager.service.delete(data)
        objects = {'result': res}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)


@token_required
@swag_from('swagger/create.yml', methods=['POST'])
@blueprint.route("/create", methods=['POST'])
def _create():
    try:
        card_schema = CardSchema()
        data = card_schema.load(request.json)
        card = object_manager.service.create(data)
        objects = {'card': card}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e
