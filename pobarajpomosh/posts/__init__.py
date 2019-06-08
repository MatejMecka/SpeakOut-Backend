from flask import Blueprint
posts_bp = Blueprint('posts', __name__)

from pobarajpomosh.posts import views
#import poborajpomosh.auth.models
import pobarajpomosh.posts.models
