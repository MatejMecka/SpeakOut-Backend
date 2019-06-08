"""
test_notifications/test_notifications.py

Test all the Notifications views
"""
from tests.base import BaseTestCase
import json
import mock

class TestControllers(BaseTestCase):
    def test_notifications_missing_field(self):
        """
        Test if notifications works correctly without a token
        """
        response = self.app.test_client().get('/notifications/api/getNotifications', content_type='application/json')
        self.assertEqual(json.loads(response.data),{"error": "Access Denied!"})

    def test_notifications_list(self):
        """
        Test if notifications works correctly listing them
        """
        # Create New Account
        response = self.app.test_client().post('/auth/api/login', json={'username':'milche', 'password':'muzikalnatamilche'}, content_type='application/json')
        data = json.loads(response.data)

        # Test it out
        response = self.app.test_client().get('/notifications/api/getNotifications?token={}'.format(data['token']),content_type='application/json')
        print('RESPONSE DATA FROM NOTIFICATIONS: ' + str(response.data))
        self.assertEqual(json.loads(response.data),{'notifications': [[], {}]})

    def test_token_push_missing_field(self):
        """
        Test if getting a token with a missing field throws an error
        """
        response = self.app.test_client().post('/notifications/api/pushToken', json={'deviceId':'nesh'}, content_type='application/json')
        self.assertEqual(json.loads(response.data),{"error": "A Field is missing!"})

    def test_token_push_invalid_token(self):
        """
        Test if pushing notification token without a valid user token will throw an error
        """
        response = self.app.test_client().post('/notifications/api/pushToken', json={'deviceId':'nesh', 'token':'Banana'}, content_type='application/json')
        self.assertEqual(json.loads(response.data),{"error": "Access Denied!"})

    def test_token_push(self):
        """
        Test token pushing from expo to backend
        """
        # Create New Account
        response = self.app.test_client().post('/auth/api/login',
                                               json={'username': 'milche', 'password': 'muzikalnatamilche'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Submit Token
        response = self.app.test_client().post('/notifications/api/pushToken',
                                              json={'deviceId': 'nesh', 'token': data['token']},
                                              content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Success'})

        # Resubmit to verify that the token has been updated
        response = self.app.test_client().post('/notifications/api/pushToken',
                                  json={'deviceId': 'nesh', 'token': data['token']},
                                  content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Success'})

    def test_token_push_no_registered_device(self):
        """
        Test token pushing from expo to backend
        """
        # Create New Account
        response = self.app.test_client().post('/auth/api/signup',
                                               json={'username': 'kompir', 'password': 'tarabuka'},
                                               content_type='application/json')
        data = json.loads(response.data)

        # Submit Token
        response = self.app.test_client().post('/notifications/api/pushToken',
                                               json={'deviceId': 'nesh', 'token': data['token']},
                                               content_type='application/json')
        self.assertEqual(json.loads(response.data), {'code': 'Success'})

    @mock.patch('requests.get')
    def test_send_notification(self, mock_get):
        """
        Test Sending Notification
        """
        from pobarajpomosh.notifications.views import sendNotification
        mock_get.return_value.status_code = 200
        notification = sendNotification('token', 'title', 'message')
        notification1 = sendNotification('token', 'title', 'message', extraData={'nesh':'nesh'}, channelID='test')
        self.assertEqual(notification, 200)
        self.assertEqual(notification1, 200)
 
