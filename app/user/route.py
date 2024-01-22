import json
from marshmallow import ValidationError
from datetime import datetime
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request
from app.user.containers import Managers
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
@token_required
def create():
    try:
        time__ = datetime.now()
        formatted_time = time__.strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'email': request.json['email'],
            'password': request.json['password'],
            'date_created': formatted_time,
            'date_modified': formatted_time
        }
        new_user__ = object_manager.service.create(data)
        objects = {'status': "success"}
        return json.dumps(objects, indent=4), 200, {'ContentType': 'application/json'}
    except Exception as e:
        raise e

@swag_from('swagger/login.yml', methods=['POST'])
@blueprint.route("/login", methods=['POST'])
def login():
    try:
        data = {
            'email': request.json['email'],
            'password': request.json['password']
        }
        token= object_manager.service.login(data)
        #card_manager.service.update(login_user.id)
        #kullancı sıstmede kayıtlı son kayıt tarıhı  olanı al ve passıve olanı sec bu sartlara uyan kayıttakı card passivede active cek
        #objects = {'services': login_user}

        return {'token': token},200
    except Exception as e:
        raise e

