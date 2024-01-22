from flask import jsonify
from flask_marshmallow import exceptions as marshmallow_exceptions
from flask_sqlalchemy import SQLAlchemy
from http.client import HTTPException
from pymysql import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError as SQLAlchemyIntegrityError
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

db = SQLAlchemy()

def handle_value_error(error: ValueError) -> tuple:
    error_message = f"Value error: {str(error)}"
    response = {
        'error': {
            'message': error_message,
            'status_code': 400
        }
    }
    return jsonify(response), 400

def handle_no_result_found(error: NoResultFound) -> tuple:
    error_message = 'No result found'
    response = {
        'error': {
            'message': error_message,
            'status_code': 404
        }
    }
    return jsonify(response), 404

def handle_multiple_results_found(error: MultipleResultsFound) -> tuple:
    error_message = 'Multiple results found'
    response = {
        'error': {
            'message': error_message,
            'status_code': 500
        }
    }
    return jsonify(response), 500

def handle_generic_error(error):
    if isinstance(error, HTTPException):
        status_code = error.code
    elif isinstance(error, (MarshmallowValidationError, ValidationError)):
        # Handle Marshmallow validation error separately
        return handle_marshmallow_validation_error(error)
    elif isinstance(error, (IntegrityError, SQLAlchemyIntegrityError)):
        # Handle IntegrityError from SQLAlchemy
        return handle_integrity_error(error)
    elif isinstance(error, NoResultFound):
        # Handle NoResultFound from SQLAlchemy
        return handle_no_result_found(error)
    elif isinstance(error, MultipleResultsFound):
        # Handle MultipleResultsFound from SQLAlchemy
        return handle_multiple_results_found(error)
    elif isinstance(error, SQLAlchemyError):
        # Handle general SQLAlchemy error
        status_code = 500
    elif isinstance(error, ValueError):
        # Handle ValueError separately
        return handle_value_error(error)
    elif isinstance(error, KeyError):
        # Handle KeyError separately
        return handle_key_error(error)
    else:
        # Handle other error types with a general status code
        status_code = 500

    # Get the error message
    error_message = str(error)

    # Prepare the response
    response = {
        'error': {
            'message': error_message,
            'status_code': status_code
        }
    }

    # Return the response in JSON format
    return jsonify(response), status_code
