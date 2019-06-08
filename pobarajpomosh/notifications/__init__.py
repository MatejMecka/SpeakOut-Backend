from flask import Blueprint
notifications_bp = Blueprint('notifications', __name__)

from pobarajpomosh.notifications import views
import pobarajpomosh.notifications.models
