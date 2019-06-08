from flask import Blueprint
volunteers_bp = Blueprint('volunteers', __name__)

from pobarajpomosh.volunteers import views, events
import pobarajpomosh.volunteers.models
