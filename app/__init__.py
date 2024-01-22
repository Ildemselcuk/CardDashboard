from app.card.models import Card
from app.transactions.models import Transactions
from app.user.models import User
import os
from importlib import import_module
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger

from app.exception import handle_generic_error

basedir = os.path.abspath(os.path.dirname(__file__))
SWAGGER_TEMPLATE = {"securityDefinitions": {"APIKeyHeader": {
    "type": "apiKey", "name": "x-access-token", "in": "header"}}}
template = {
    "swagger": "2.0",
    "info": {
        "title": "XYZ API Docs",
        "description": "API Documentation for XYZ Application",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "XYZ@XYZ.com",
            "url": "XYZ.com",
        },
        "termsOfService": "XYZ .com",
        "version": "1.0"
    },
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "token": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "\
            JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger_config = {
    "headers": [

    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apispec"
}
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
swagger = Swagger(template=template, config=swagger_config)


def register_extensions(app):

    db.init_app(app)
    ma.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)


def configure_database(app):
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_blueprints(app):
    for module_name in ('card', 'transactions', 'user'):
        module = import_module('app.{}.route'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_error_handler(Exception, handle_generic_error)
    register_blueprints(app)
    register_extensions(app)
    configure_database(app)
    return app
