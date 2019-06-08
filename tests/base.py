"""
tests/base.py

The Base for all Tests Cased used during all the module in tests
"""
from flask_testing import TestCase
from pobarajpomosh.auth.models import User, Role
from pobarajpomosh.posts.models import Post, Comment
from pobarajpomosh.volunteers.models import ChatSessionsCounter, MessageCounter
from pobarajpomosh.notifications.models import DevicesNotificationHandlers

from pobarajpomosh import db, create_app
import uuid

class BaseTestCase(TestCase):

	# executed prior to each test
	def create_app(self):
		app = create_app()
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		db.create_all()

		# Create Database Records
		roles = [Role(name="Administrator"), Role(name="Moderator"), Role(name="Volunteer"), Role(name="User")]

		user1 = User(username='randomusername', role_id=4, approved=0, token=str(uuid.uuid4().hex))
		user1.hash_password('randompassword')
		user2 = User(username='milche', role_id=1, approved=0, token=str(uuid.uuid4().hex))
		user2.hash_password('muzikalnatamilche')
		user3 = User(username='kiseli-krstavichki', role_id=1, approved=1,
					 token=str(uuid.uuid4().hex))  # Samo za Aksa ova... Vidi Facebook
		user3.hash_password('krstavicaniedna')
		users = [user1, user2, user3]

		device = DevicesNotificationHandlers(user_id=2, notificationToken='ExponentPushToken[NESHO]')
		device1 = DevicesNotificationHandlers(user_id=3, notificationToken='ExponentPushToken[NESHO]')
		devices = [device, device1]

		messageCount = MessageCounter()
		chatSessionCount = ChatSessionsCounter()

		db.session.add_all(roles)
		db.session.add(messageCount)
		db.session.add(chatSessionCount)
		db.session.add_all(users)
		db.session.add_all(devices)
		
		db.session.commit()


	def makePost(self, data):
		user = User.query.filter_by(token=data['token']).first()
		post = Post(author_id=user.id, title=data['title'], body=data['body'], category=data['category'], approved=data['approved'], likes=0)
		db.session.add(post)
		db.session.commit()

		return post.id

	def makeComment(self, data):
		user = User.query.filter_by(token=data['token']).first()
		comment = Comment(author_id=user.id, post_id=data['post_id'], body=data['body'], approved=data['approved'], likes=0)
		db.session.add(comment)
		db.session.commit()

		return comment.id


	def tearDown(self):
		db.session.remove()
		db.drop_all()



