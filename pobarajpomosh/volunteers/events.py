from pobarajpomosh import socketio, db
from pobarajpomosh.auth.models import User
from pobarajpomosh.volunteers.views import send_slack_message
from flask_socketio import emit, join_room, leave_room
from pobarajpomosh.volunteers.models import Message, MessageCounter


@socketio.on('joined', namespace='/chat')
def joined(message, room, name):
    """
    Sent by clients when they enter a room.
    A status message is broadcast to all people in the room.
    """
    send_slack_message('{} joined the room!'.format(name), room)
    join_room(room)
    emit('status', {'msg': str(message) + ' has entered the room.', 'username': 'АндроМета'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message, room, name):
    """
    Sent by a client when the user entered a new message.
    The message is sent to all people in the room.
    """

    # Statistic Purpose Code here
    counter = MessageCounter.query.first()
    counter.count += 1
    db.session.commit()

    # Get User to store username
    user = User.query.filter_by(username=name).first().id

    # Store Messages
    msg = Message(user_id=user, message=message['msg'], room=room, volunteer='none')
    db.session.add(msg)
    db.session.commit()

    emit('message', {'msg': message['msg'], 'username': name}, room=room)
    send_slack_message('{}: {}'.format(name, message['msg']), room)
