"""
notifications/views.py

Handle All Notification related procedures :)
"""
from flask import render_template, request, jsonify
from pobarajpomosh.auth.models import User
from pobarajpomosh.notifications import notifications_bp
from pobarajpomosh.notifications.models import Notifications, notification_schema, DevicesNotificationHandlers
from pobarajpomosh.decorators import check_valid_token, check_missing_fields
from pobarajpomosh import db
from sqlalchemy import desc
import requests
import json


@notifications_bp.route('/api/getNotifications', methods=['GET'])
def list_notifications():
    """
    <url>/notifications/api/getNotifications

    List posts based on the category assigned
    """
    token = request.args.get('token')
    user = User.query.filter_by(token=token).first()

    if user is None:
        return jsonify({"error": "Access Denied!"})

    # Filter Posts so the user doesn't have to filter it
    notifications = Notifications.query.filter_by(user_id=user.id).order_by(desc('created'))
    result = notification_schema.dump(notifications)

    # Notifications have been read delete them
    toDelete = Notifications.query.filter_by(user_id=user.id)
    toDelete.delete()

    return jsonify({
        "notifications": result
    })


@notifications_bp.route('/api/pushToken', methods=['POST'])
@check_missing_fields(["token", "deviceId"])
@check_valid_token
def post_token():
    """
    <url>/notifications/api/PushToken

    Get Device Tokens for notifications
    """
    token = request.json.get('token')
    deviceId = request.json.get('deviceId')

    user = User.query.filter_by(token=token).first()
    device = DevicesNotificationHandlers.query.filter_by(user_id=user.id).first()

    if device is None:
        # Device doesn't exist for that user create a new one
        device = DevicesNotificationHandlers(user_id=user.id, notificationToken=deviceId)
    else:
        # Device does Exist for that user update it to use the latest device
        device.notificationToken = deviceId

    db.session.add(device)
    db.session.commit()
    return jsonify({'code': 'Success'})



def sendNotification(token, title, message, extraData=None, channelID=None):
    """
    send Notification to Devices

    :param token:
    :param title:
    :param message:
    :return:
    """
    url = 'https://exp.host/--/api/v2/push/send'

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "to": token,
        "title": title,
        "body": message
    }

    # Verify we have Additional data to append
    if extraData is not None:
        data["data"] = extraData

    # Android Only! Verify if we have a channel ID and append it
    if channelID is not None:
        data["channelId"] = channelID

    res = requests.post(url, data=json.dumps(data), headers=headers)
    return res.status_code
