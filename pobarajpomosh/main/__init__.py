"""
main/__init__.py

Register Blueprint
"""
from flask import Blueprint
main_bp = Blueprint('main', __name__)

from pobarajpomosh.main import views
