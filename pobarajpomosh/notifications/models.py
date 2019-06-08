"""
models.py

Responsible for Handling the Notification models
"""
import datetime
from .. import db, ma


class Notifications(db.Model):
    """
    Store all the Notifications for a User
    """
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(1024), nullable=False)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.datetime.utcnow)

    def __repr__(self):
        return'<Notification {}>'.format(self.id)


class DevicesNotificationHandlers(db.Model):
    """
    Register Device and Expo Token
    """
    __tablename__ = "usersanddevicestokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notificationToken = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return'<Device {}>'.format(self.id)


class NotificationSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'user_id', 'title', 'body', 'created')


notification_schema = NotificationSchema(many=True)
