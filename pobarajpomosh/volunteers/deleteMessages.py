"""
volunteers/deleteMessages.py

Delete all Messages set on a date
"""


from pobarajpomosh.volunteers.models import Message
from pobarajpomosh import db
import datetime
import os

messages = Message.query.all()
current_date = datetime.datetime.utcnow()

def deleteMessages():
    """
    Delete all the messages from the database
    """
    for message in messages:
        remaining_time = current_date - message.created
        if remaining_time.days > os.environ['MESSAGE_RETENTION']:
            db.session.delete(message)
            db.session.commit()

if __name__ == '__main__':
    deleteMessages()