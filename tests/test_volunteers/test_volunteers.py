"""
test_volunteers/test_volunteers.py

Test all the Volunteer views
"""
from tests.base import BaseTestCase
from pobarajpomosh import db
from pobarajpomosh.auth.models import User
import uuid


class TestControllers(BaseTestCase):
	def test_dashboard(self):
		"""
		Test if dashboard works
		"""
		self.createData()
		with self.app.test_client() as c:
			response = c.post('/auth/login', data=dict(username='kiseli-krstavichki', password='krstavicaniedna',submit=True, follow_redirects=True))
			response = c.get('/volunteers/reports')
			self.assertEqual(response.status_code, 200)
			self.assert_template_used('reports.html')

	def test_dashboard_insufficent_permissions(self):
		"""
		Test if dashboard works
		"""
		self.createData()
		with self.app.test_client() as c:
			response = c.post('/auth/login', data=dict(username='randomusername', password='randompassword',submit=True, follow_redirects=True))
			response = c.get('/volunteers/reports')
			self.assertEqual(response.status_code, 403)

	def createData(self):
		"""
		Create Post and Comments because reasons
		:return:
		"""
		# Create User to log in
		token = str(uuid.uuid4().hex)
		user = User(username='danche', role_id=4, token=token, approved=1)
		user.hash_password('dancingdanche')  # :))

		# Commit User
		db.session.add(user)
		db.session.commit()

		# Make Post
		data = {
			"token": token,
			"title": "Test",
			"body": "Testing 1,2,3",
			"category": "1"
		}

		response = self.app.test_client().post('/posts/api/post/create', json=data, content_type='application/json')

		# Create Comment
		data = {
			"token": token,
			"body": "Testing 1,2,3",
			"post_id": 1
		}

		response = self.app.test_client().post('/posts/api/comment/create', json=data, content_type='application/json')