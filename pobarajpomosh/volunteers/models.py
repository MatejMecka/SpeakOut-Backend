"""
models.py

Responsible for Handling the Volunteers

"""
from sqlalchemy import Column, Integer, String, Text, DateTime
import datetime
from .. import db, ma


class ChatSessionsCounter(db.Model):
    """
    Count How Many chat sessions have been made
    """
    __tablename__ = "chatsessioncounter"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False, default=0)


class MessageCounter(db.Model):
    """
    Count How Many messages have been sent
    """
    __tablename__ = "messagescounter"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False, default=0)


class UserChatRelationship(db.Model):
    """
    Map the User, Room relationships
    """
    __tablename__ = "userchatrelationship"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room = db.Column(db.String(1024), nullable=False)
    volunteer_id = db.Column(db.String(1024)) # Use References from Slack

class Message(db.Model):
    """
    Message Model for storing Messages
    """
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(1024), nullable=False)
    room = db.Column(db.String(1024), nullable=False)
    volunteer = db.Column(db.String(1024), nullable=False)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.datetime.utcnow)

    def __repr__(self):
        return'<Message {}>'.format(self.id)


class MessageSchema(ma.Schema):
    """
    Marshmallow Schema for representing message objects in JSON
    """
    class Meta:
        # Fields to expose
        fields = ('id', 'user_id', 'message', 'volunteer', 'created')


messages_schema = MessageSchema(many=True)
