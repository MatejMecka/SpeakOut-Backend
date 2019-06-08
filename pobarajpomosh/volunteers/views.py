"""
volunteers/views.py

Controller Responsible for Handling the chat and volunteer parts

"""

import string, random, os
from flask import render_template, request, jsonify, session
from flask_login import login_required
from pobarajpomosh.volunteers import volunteers_bp
from pobarajpomosh.auth.models import User
from pobarajpomosh.volunteers.models import Message, ChatSessionsCounter, MessageCounter, UserChatRelationship, messages_schema
from pobarajpomosh.posts.models import Post, Comment
from pobarajpomosh.notifications.models import DevicesNotificationHandlers
from pobarajpomosh.notifications.views import sendNotification
from pobarajpomosh.decorators import check_access_rights, check_missing_fields, check_valid_token
from sqlalchemy import desc
from pobarajpomosh import db, sc, socketio
from collections import OrderedDict
from datetime import datetime

conversations = {}


def generateChartComment():
    """
    Generates data to display a Chart

    P.S This is insufficent AF, Todo: Figure out a Better way to optimize this because we will get fucked
    if we have more and more records O(n)

    :return: obj
    """
    obj = {}
    # Get All Posts and build a Object out of dates
    for comment in Comment.query.all():
        if comment.created.strftime("%d-%m-%Y") in obj:
            obj[comment.created.strftime("%d-%m-%Y")] += 1
        else:
            obj[comment.created.strftime("%d-%m-%Y")] = 1
    return obj


def generateChartPost():
    """
    Generates data to display a Chart

    P.S This is insufficent AF, Todo: Figure out a Better way to optimize this because we will get fucked
    if we have more and more records O(n)

    :return: obj
    """
    obj = {}
    # Get All Posts and build a Object out of dates
    for post in Post.query.all():
        if post.created.strftime("%d-%m-%Y") in obj:
            obj[post.created.strftime("%d-%m-%Y")] += 1
        else:
            obj[post.created.strftime("%d-%m-%Y")] = 1
    return obj


@volunteers_bp.route('/dashboard', methods=['GET'])
@login_required
@check_access_rights([1, 2])
def dashboard():
    userCount = db.session.query(User).count()
    postCount = db.session.query(Post).count()
    commentCount = db.session.query(Comment).count()
    messageCount = MessageCounter.query.first().count
    chatSessions = ChatSessionsCounter.query.first().count

    # Generate Chart.JS Data for Posts
    chartPostData = generateChartPost()
    chartPostData = OrderedDict(sorted(chartPostData.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y')))
    postLabels = list(chartPostData.keys())
    postValues = list(chartPostData.values())

    # Generate Chart.JS Data for Comments
    chartCommentData = generateChartComment()
    chartCommentData = OrderedDict(sorted(chartCommentData.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y')))
    commentLabels = list(chartCommentData.keys())
    commentValues = list(chartCommentData.values())

    return render_template('dashboard.html', userCount=userCount, postCount=postCount,
                           messageCount=messageCount, chatSessions=chatSessions, commentCount=commentCount,
                           chartPostLabels=postLabels, chartPostValues=postValues, postMax=max(postValues),
                           chartCommentLabels=commentLabels, chartCommentValues=commentValues, commentMax=max(commentValues))


@volunteers_bp.route('/reports', methods=['GET'])
@login_required
@check_access_rights([1, 2])
def reports():
    """
    Report Page, Where all flagged posts appear

    :return:
    """
    reportPosts = Post.query.filter_by(reported=1, approved=1).order_by(desc('created')).limit(300)
    reportComments = Comment.query.filter_by(reported=1, approved=1).order_by(desc('created')).limit(300)
    return render_template('reports.html', posts=reportPosts, comments=reportComments)


def send_slack_message(message, channel):
    """
    Sends Slack Messages

    :param message: The Message to send
    :param channel: The Channel to send it to
    :return:
    """
    sc.chat_postMessage(
        channel=channel,
        text=message,
        icon_emoji=':robot_face:',
        username='volonterko'
    )


@volunteers_bp.route('/chat', methods=['GET'])
def chat():
    """
    The Chat the users use to communicate with the Volunteers

    :return:
    """
    return render_template('newChat.html')


@volunteers_bp.route('/slack', methods=['POST'])
def slack_webhook():
    """
    <url>/volunteers/slack

    Handle Events From Slack
    """
    payload = request.get_json()
    print(payload)

    if payload['token'] != os.environ['SLACK_VERIFICATION_TOKEN']:
        return jsonify({"error": "Verification failed!"})

    # Used for setting up
    if payload['type'] == "url_verification":
        return jsonify({"challenge": payload['challenge']})

    if payload['event']['type'] == "message":
        if payload['event']['text'].startswith('!join'):
            channel = payload['event']['text'][6:22]

            # Get the Users chat session
            chatSession = UserChatRelationship.query.filter_by(room=channel).first()

            # Verify if someone has taken it
            if chatSession.volunteer_id is not None:
                message = "*ACCESS DENIED!* <@{}> is participating in this conversation!".format(
                    chatSession.volunteer_id)
                send_slack_message(message, os.environ['SLACK_VOLUNTEERS_CHAT_ID'])
            else:
                # Invite To Channel
                sc.groups_invite(
                    channel=channel,
                    user=payload['event']['user']
                )

                message = "<@{}> Has accepted the conversation!".format(payload['event']['user'])
                send_slack_message(message, os.environ['SLACK_VOLUNTEERS_CHAT_ID'])

                chatSession.volunteer_id = payload['event']['user']
                db.session.commit()

            return '200'
        elif payload['event']['channel'][0] == "G":
            # Get Channel ID and redirect it
            channel = payload['event']['channel']

            # Verify this is not actually the bot relaying the messages
            if 'user' in payload['event']:
                # Relay Message to Socket
                message = '{}'.format(payload['event']['text'])
                socketio.emit('message', {'msg': message}, room=str(channel), namespace='/chat', username='username')

                # Statistic Purposes here
                counter = MessageCounter.query.first()
                counter.count += 1
                db.session.commit()

                # Get User
                user = UserChatRelationship.query.filter_by(room=str(channel)).first().user_id

                # Store Messages
                message = Message(user_id=user, message=message, room=str(channel), volunteer='username')
                db.session.add(message)
                db.session.commit()

                # Get The User to send the notification too
                device = DevicesNotificationHandlers.query.filter_by(user_id=user).first()

                # Send a Notification if we have a valid user with a valid notificationToken
                if device is not None:
                    token = device.notificationToken
                    title = "Имаш порака од Волонтер!"
                    body = "Имате Повратен одговор од нашиот волонтер!"
                    sendNotification(token, title, body)
                return 'hello'
    # Default
    return 'Hello!'


@volunteers_bp.route('/api/generatechat', methods=['POST'])
@check_missing_fields(["token"])
@check_valid_token
def generate_chat():
    """
    <url>/volunteers/api/generatechat

    Generate a Chat Id to connect a user to
    """
    token = request.json.get('token')
    user = User.query.filter_by(token=token).first()

    # Generate a random channel name
    chars = string.ascii_uppercase + string.digits
    channelId = ''.join(random.choice(chars) for _ in range(6))

    # Create a Channel
    channel = sc.api_call(
        "groups.create",
        json={
            'name': channelId
        }
    )

    message = "<!channel> User({}) has Requested to chat with a volunteer! " \
              "Please message this channel with" \
              " `!join {}` to begin a conversation with them!".format(user.username, channel['group']['id'])

    send_slack_message(message, os.environ['SLACK_VOLUNTEERS_CHAT_ID'])

    # Increment Counter for statistics
    counter = ChatSessionsCounter.query.first()
    counter.count += 1
    db.session.commit()

    # Map The Relationship
    relationship = UserChatRelationship(user_id=user.id, room=channel['group']['id'])  # <3
    db.session.add(relationship)
    db.session.commit()

    return jsonify({'channel_id': channel['group']['id']})



@volunteers_bp.route('/api/messages/list/user', methods=['GET'])
def list_messages_by_user():
    """
    <url>/api/messages/list/user

    View that Lists all the messages by user
    """
    limit = request.args.get('length', default=25)
    room = request.args.get('room')
    token = request.args.get('token')

    user = User.query.filter_by(token=token).first()

    if user is None:
        return jsonify({"error": "Access Denied!"})

    if room is None:
        return jsonify({'error': 'Room has not been selected! Please enter the room number followed by the access code'})

    messages = Message.query.filter_by(user_id=user.id, room=room).limit(limit)
    result = messages_schema.dump(messages)

    return jsonify({
        "messages": result
    })
