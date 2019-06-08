"""
decorators.py

Decorators used most often
"""
from functools import wraps
from flask import abort, jsonify, request
from flask_login import current_user
from pobarajpomosh.auth.models import User

def check_access_rights(roles=[], parent_route=None):
    """
    Decorator that checks if a user can access the page.
    :param roles: A list of roles that can access the page.
    :type roles: list[str]
    :param parent_route: If the name of the route isn't a regular page (e.g. for ajax request handling), pass the name
    of the parent route.
    :type parent_route: str
    """
    def access_decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            route = parent_route
            if route is None:
                route = request.endpoint
            elif route.startswith("."):
                # Relative to current blueprint, so we'll need to adjust
                route = request.endpoint[:request.endpoint.rindex('.')] + route
                # Todo: Maybe Refactor this
            if request.is_json is False:
                if current_user.role_id in roles:
                    return fn(*args, **kwargs)
                # Return page not allowed
                abort(403, request.endpoint)
            elif User.query.filter_by(token=request.json.get('token')).first().role_id in roles:
                return fn(*args, **kwargs)
            return jsonify({'error':'Access Denied!'})

        return decorated_function

    return access_decorator


def check_valid_token(fn):
    """
    Decorator that checks if a token is valid
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        token = request.json.get('token')
        user = User.query.filter_by(token=token).first()
        if user is None:
            return jsonify({"error": "Access Denied!"})
        return fn(*args, **kwargs)
    return decorated_function

def check_valid_method(fn):
    """
    Decorator that checks if a token is valid
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if request.path.split('/')[3] == 'post' or request.path.split('/')[3] == 'comment':
            return fn(*args, **kwargs)
        abort(404)
    return decorated_function

def check_missing_fields(fields=[]):
    """
    Decorator that checks if a field is missing.
    :param fields: A list of fields that we need.
    """
    def access_decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            for field in fields:
                if request.json.get(field) is None:
                    return jsonify({"error": "A Field is missing!"})
            return fn(*args, **kwargs)

        return decorated_function

    return access_decorator

