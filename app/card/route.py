
import json
from datetime import datetime
from pymysql import IntegrityError
from app.card.containers import Managers
from flasgger.utils import swag_from
from flask import Blueprint, request, session
from app.card.models import CardSchema, DeleteCardSchema, DetailListCardSchema
from app.user.utils import token_required

# initialize object manager
object_manager = Managers.object_manager()

blueprint = Blueprint(
    'card',
    __name__,
    url_prefix='/card'
)


@blueprint.route("/list", methods=['GET'])
@swag_from('/app/card/swagger/list.yml', methods=['GET'])
@token_required
def _list():
    try:
        result = object_manager.service.list()
        _serialized = CardSchema(many=True).dump(result)
        objects = {'cards': _serialized}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@blueprint.route("/detail_list", methods=['GET'])
@swag_from('/app/card/swagger/detail_list.yml', methods=['GET'])
@token_required
def _detail_list():
    try:
        _schema = DetailListCardSchema()
        data = _schema.load(request.args)
        cards = CardSchema(many=True).dump(
            object_manager.service.detail_list(data))
        objects = {'cards': cards}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@blueprint.route("/update/<card_no>", methods=['PUT'])
@swag_from('/app/card/swagger/update.yml', methods=['PUT'])
@token_required
def _update(card_no):
    try:
        card_schema = CardSchema()
        data = card_schema.load(request.json)
        current = {
            "user_id": session.get("current_user", {}).get("user_id", None),
            "card_no": card_no
        }
        services = object_manager.service.update(data, current)
        return json.dumps({'updated': services}, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@blueprint.route("/delete/<card_no>", methods=['DELETE'])
@swag_from('/app/card/swagger/delete.yml', methods=['DELETE'])
@token_required
def _delete(card_no):
    try:
        _schema = DeleteCardSchema()
        data = _schema.load({"card_no": card_no})
        res = object_manager.service.delete(data)
        objects = {'result': "success"}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@blueprint.route("/create", methods=['POST'])
@swag_from('/app/card/swagger/create.yml', methods=['POST'])
@token_required
def _create():
    try:
        card_schema = CardSchema()
        data = card_schema.load(request.json)
        data["user_id"] = session["current_user"]["user_id"]
        card = object_manager.service.create(data)
        objects = {'card': card}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e
