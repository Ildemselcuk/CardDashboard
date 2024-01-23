import json
from flasgger.utils import swag_from
from flask import Blueprint, request
from app.user.containers import Managers
from app.user.models import LoginSchema, UserSchema
from app.user.utils import token_required 

# Start listening events
object_manager = Managers.object_manager()


blueprint = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)

@swag_from('swagger/create.yml', methods=['POST'])
@blueprint.route("/create", methods=['POST'])
def create():
    try:
        _schema = UserSchema()
        data = _schema.load(request.json)
        object_manager.service.create(data)
        objects = {'status': "success"}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e


@swag_from('swagger/login.yml', methods=['POST'])
@blueprint.route("/login", methods=['POST'])
def login():
    try:
        _schema = LoginSchema()
        data = _schema.load(request.json)
        token= object_manager.service.login(data)
        return {'token': token}, 200
    except Exception as e:
        raise e

