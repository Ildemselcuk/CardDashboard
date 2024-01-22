from flask import jsonify
from flask_marshmallow import exceptions as marshmallow_exceptions
from flask_sqlalchemy import SQLAlchemy
from http.client import HTTPException
from marshmallow import ValidationError
from pymysql import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError as SQLAlchemyIntegrityError
from marshmallow.exceptions import ValidationError as MarshmallowValidationError


def handle_marshmallow_validation_error(error: MarshmallowValidationError) -> tuple:
    # Create a custom response for Marshmallow validation error
    error_messages = error.messages
    response = {
        'error': {
            'message': 'Validation error',
            'errors': error_messages,
            'status_code': 400
        }
    }
    return jsonify(response), 400


def handle_integrity_error(error: SQLAlchemyIntegrityError) -> tuple:
    # Create a custom response for SQLAlchemy IntegrityError
    error_message = 'Integrity error: Duplicate entry or constraint violation'
    response = {
        'error': {
            'message': error_message,
            'status_code': 409
        }
    }
    return jsonify(response), 409


def handle_no_result_found(error: NoResultFound) -> tuple:
    # Create a custom response for NoResultFound error
    error_message = 'No result found'
    response = {
        'error': {
            'message': error_message,
            'status_code': 404
        }
    }
    return jsonify(response), 404


def handle_multiple_results_found(error: MultipleResultsFound) -> tuple:
    # Create a custom response for MultipleResultsFound error
    error_message = 'Multiple results found'
    response = {
        'error': {
            'message': error_message,
            'status_code': 500
        }
    }
    return jsonify(response), 500


def handle_value_error(error: ValueError) -> tuple:
    # Create a custom response for ValueError
    error_message = f"Value error: {str(error)}"
    response = {
        'error': {
            'message': error_message,
            'status_code': 400
        }
    }
    return jsonify(response), 400


def handle_key_error(error: KeyError) -> tuple:
    # Create a custom response for KeyError
    error_message = f"Key error: {str(error)}"
    response = {
        'error': {
            'message': error_message,
            'status_code': 400
        }
    }
    return jsonify(response), 400


def handle_generic_error(error):
    # Handle general error situation
    if isinstance(error, HTTPException):
        status_code = error.code
    elif isinstance(error, (MarshmallowValidationError, ValidationError)):
        # Handle Marshmallow validation error separately
        return handle_marshmallow_validation_error(error)
    elif isinstance(error, (IntegrityError, SQLAlchemyIntegrityError)):
        # Handle SQLAlchemy Integrity error separately
        return handle_integrity_error(error)
    elif isinstance(error, NoResultFound):
        # Handle SQLAlchemy NoResultFound error separately
        return handle_no_result_found(error)
    elif isinstance(error, MultipleResultsFound):
        # Handle SQLAlchemy MultipleResultsFound error separately
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
