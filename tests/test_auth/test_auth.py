"""
test_auth/test_auth.py

Test all the Authentication views
"""
from tests.base import BaseTestCase
import json
import uuid
from pobarajpomosh import db
from pobarajpomosh.auth.models import User

class TestControllers(BaseTestCase):
	def test_login(self):
		"""
		Test if login works correctly
		"""
		response = self.app.test_client().post('/auth/api/login', json={'username':'randomusername', 'password':'randompassword'}, content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(data['code'],"success")

	def test_login_missing_field(self):
		"""
		Test if login works correctly without a field
		"""
		response = self.app.test_client().post('/auth/api/login', json={'username':'randomusername'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error":"A Field is missing!"})


	def test_login_invalid_credentials(self):
		"""
		Test if login works correctly without a correct password
		"""
		response = self.app.test_client().post('/auth/api/login', json={'username':'randomusername', 'password':'radnompassword'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error":"Username or Password incorrect!"})

	def test_login_wrong_username(self):
		"""
		Test if login works correctly without a correct password
		"""
		response = self.app.test_client().post('/auth/api/login', json={'username':'mila9', 'password':'randpass'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error":"Username or Password incorrect!"})

	def test_signup_missing_field(self):
		"""
		Test if signup works correctly without a field
		"""
		response = self.app.test_client().post('/auth/api/signup', json={'username':'randomusername'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error":"A Field is missing!"})

	def test_signup(self):
		"""
		Test if signup works correctly without a correct password
		"""
		response = self.app.test_client().post('/auth/api/signup', json={'username':'mila1', 'password':'password'}, content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(data['code'],'Registration Succesful!')

	def test_signup_user_exists(self):
		"""
		Test if signup works correctly with an existing user
		"""
		response = self.app.test_client().post('/auth/api/signup', json={'username':'randomusername', 'password':'mirko'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error":"User already exists!"})

	def test_approve_user(self):
		"""
		Test User approval
		"""
		# Login
		loginData = {
			"username": "milche",
			"password":  "muzikalnatamilche"
		}

		responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')

		loginData = json.loads(responseLogin.data)
		token = loginData['token']
		response = self.app.test_client().post('/auth/api/approve', json={"token": token, "user": "1"}, content_type='application/json')
		self.assertEqual(json.loads(response.data), {'code': 'Approval Succesful!'})

		# Test Wrong User ID
		response = self.app.test_client().post('/auth/api/approve', json={"token": token, "user": "113434"}, content_type='application/json')
		self.assertEqual(json.loads(response.data), {"error": "Invalid User"})

	def test_approve_user_invalid_permission(self):
		"""
		Test without proper permission
		"""
		# Get Token
		resp = self.app.test_client().post('/auth/api/signup', json={'username':'mila1', 'password':'password'}, content_type='application/json')
		data = json.loads(resp.data)

		# Test Approval
		response = self.app.test_client().post('/auth/api/approve', json={"token": data["token"], "user": "1"}, content_type='application/json')
		self.assertEqual(json.loads(response.data), {'code': 'Access Denied!'})

	def test_approve_user_invalid_token(self):
		"""
		Test if signup works correctly with an existing user
		"""
		response = self.app.test_client().post('/auth/api/approve', json={'token': 'OvaENeValidenTokenAkoNePrimeti', 'user': '1'}, content_type='application/json')
		print(response)
		self.assertEqual(json.loads(response.data),{'error': 'Access Denied!'})

	def test_approve_user_missing_field(self):
		"""
		Test if signup works correctly with an existing user
		"""
		response = self.app.test_client().post('/auth/api/approve', json={'token': 'OvaENeValidenTokenAkoNePrimeti'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error": "A Field is missing!"})

	def test_login_page(self):
		"""
		Test if Login page works
		"""
		self.createData()
		response = self.app.test_client().post('/auth/login', data=dict(username='nesho',password='nesho', submit=True), follow_redirects=True)
		self.assertIn('Incorrect Email or Password!', str(response.data))
		response = self.app.test_client().post('/auth/login',
											   data=dict(username='kiseli-krstavichki', password='krstavicaniedna', submit=True),
											   follow_redirects=True)
		self.assert_template_used('dashboard.html')
		#self.assertRedirects(response,'/volunteers/dashboard')

	def test_logout_page(self):
		"""
		Test if Logout page works
		"""
		response = self.app.test_client().get('/auth/logout', follow_redirects=True)
		self.assertIn('Logout Successful!', str(response.data))

	def test_get_username_missing_field(self):
		"""
		Test if getting username with a missing field will throw an error
		"""
		response = self.app.test_client().post('/auth/api/user', json={'token': 'OvaENeValidenTokenAkoNePrimeti'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error": "A Field is missing!"})

	def test_get_username_invalid_token(self):
		"""
		Test if getting username with a missing field will throw an error
		"""
		response = self.app.test_client().post('/auth/api/user', json={'token': 'OvaENeValidenTokenAkoNePrimeti', 'user':'1'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error": "Access Denied!"})

	def test_get_username_from_user_id(self):
		"""
		Test if getting username with a missing field will throw an error
		"""
		# Login
		loginData = {
			"username": "milche",
			"password": "muzikalnatamilche"
		}

		responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')

		loginData = json.loads(responseLogin.data)
		token = loginData['token']
		response = self.app.test_client().post('/auth/api/user', json={"token": token, "user": "1"},
											   content_type='application/json')
		self.assertEqual(json.loads(response.data), {'username': 'randomusername'})

	def test_username_invalid_token(self):
		"""
		Test if getting username with a missing field will throw an error
		"""
		response = self.app.test_client().post('/auth/api/userinfo', json={'token': 'OvaENeValidenTokenAkoNePrimeti', 'user':'1'}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{"error": "Access Denied!"})

	def test_get_username_from_user_id(self):
		"""
		Test if getting username with a missing field will throw an error
		"""
		# Login
		loginData = {
			"username": "milche",
			"password": "muzikalnatamilche"
		}

		responseLogin = self.app.test_client().post('/auth/api/login', json=loginData, content_type='application/json')

		loginData = json.loads(responseLogin.data)
		token = loginData['token']
		response = self.app.test_client().post('/auth/api/userinfo', json={"token": token},
											   content_type='application/json')
		self.assertEqual(json.loads(response.data), {'username': 'milche'})

	def test_username_from_id(self):
		"""
		Test if getting a username from a particular user works
		"""
		# Create New Account
		response = self.app.test_client().post('/auth/api/login', json={'username':'milche', 'password':'muzikalnatamilche'}, content_type='application/json')
		data = json.loads(response.data)

		# Test it out
		response = self.app.test_client().post('/auth/api/user', json={"token": data['token'], "user":"1"}, content_type='application/json')
		self.assertEqual(json.loads(response.data),{'username': "randomusername"})

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