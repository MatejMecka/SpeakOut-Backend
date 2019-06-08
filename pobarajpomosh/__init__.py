"""
pobarajpomosh/__init__.py

Initialize the Backend, configure all connectors and attach all blueprints

"""
# Imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_marshmallow import Marshmallow
import slack
from flask_socketio import SocketIO

sentry_sdk.init(
    dsn=os.environ['SENTRY_API_KEY'],
    integrations=[FlaskIntegration()]
)
db = SQLAlchemy()
app = Flask(__name__, static_folder='static')
ma = Marshmallow(app)
socketio = SocketIO(app)

# Set up Flask_Login
login_manager = LoginManager()
login_manager.login_view = 'auth.log_in'

# Configure Flask and SQLAlchemy
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisisaprettyrandomstringusedforasecrettokenandimjustfillingupspacesoitslargeenoughtbecauseiwantittobelikethatbutyoucandowhateveryouwantandalsowhyareyoureadingthisimjustwastingyourtimeimsosorryforthat'

db = SQLAlchemy(app)

slack_token = os.environ["SLACK_API_TOKEN"]
sc = slack.WebClient(slack_token)


def create_app():
    """
    Create Flask App

    """
    db.init_app(app)
    login_manager.init_app(app)

    # Register Views
    from pobarajpomosh.main import main_bp
    app.register_blueprint(main_bp)

    from pobarajpomosh.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from pobarajpomosh.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from pobarajpomosh.volunteers import volunteers_bp
    app.register_blueprint(volunteers_bp, url_prefix='/volunteers')

    from pobarajpomosh.notifications import notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')

    return app
