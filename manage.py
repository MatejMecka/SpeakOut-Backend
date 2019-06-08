"""
manage.py

Tool that you use to Access the Database and the Backend
"""
from pobarajpomosh import create_app, db, socketio
from pobarajpomosh.auth.models import Role, User
from pobarajpomosh.posts.models import Post, Comment
from pobarajpomosh.volunteers.models import MessageCounter, ChatSessionsCounter
from pobarajpomosh.notifications.models import DevicesNotificationHandlers
from flask_migrate import Migrate, upgrade
import uuid
import string
import random

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User,
                Post=Post, Comment=Comment,
                MessageCounter=MessageCounter, ChatSessionsCounter=ChatSessionsCounter,
                DevicesNotificationHandlers=DevicesNotificationHandlers)


@app.cli.command()
def init_db():
    """
    Initialize Simple Database for starting a new instance
    """
    # Create Db
    db.drop_all()
    print('Creating database...')
    db.create_all()

    # Create Roles
    print('Creating Roles...')
    roles = [Role(name="Administrator"), Role(name="Moderator"), Role(name="Volunteer"), Role(name="User")]
    db.session.add_all(roles)

    # Create Basic Users
    print('Creating Users...')

    username = 'randomusername'
    password = 'randompassword'

    user1 = User(username=username, role_id=4, approved=0, token=str(uuid.uuid4().hex))
    user1.hash_password(password)

    print('Created User with username: {} and Password: {}'.format(username, password))

    username = 'admin'
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(15))

    user2 = User(username=username, role_id=1, approved=0, token=str(uuid.uuid4().hex))
    user2.hash_password(password)

    users = [user1, user2]

    db.session.add_all(users)
    db.session.commit()

    print('Created Admin User with username: {} and Password: {}'.format(username, password))

    # Create Posts, Comments

    print('Creating Post...')
    test = 'Hello World!'

    post = Post(author_id=1, title=test, body=test, category=1, approved=1, likes=0)

    db.session.add(post)
    db.session.commit()

    print('Creating Comment...')

    comment = Comment(author_id=1, body=test, approved=1, likes=0)

    db.session.add(comment)
    db.session.commit()

    # Create Counts

    print('Creating Message Counter and Chat Session Counter...')

    messageCount = MessageCounter()
    chatSessionCount = ChatSessionsCounter()
    db.session.add(messageCount)
    db.session.add(chatSessionCount)

    # Register Notification Token

    print('Registering Notification Token for user...')

    device = DevicesNotificationHandlers(user_id=1, notificationToken='ExponentPushToken[NESHO]')
    db.session.add(device)
    db.session.commit()

    print('Sucesfully Filled out Database!')


if __name__ == "__main__":
    socketio.run(app)
    # app.run()

