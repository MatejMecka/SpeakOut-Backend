from flask import Blueprint
auth_bp = Blueprint('auth', __name__)

from pobarajpomosh.auth import views
import pobarajpomosh.auth.models
