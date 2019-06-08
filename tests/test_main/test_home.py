from tests.base import BaseTestCase

class TestControllers(BaseTestCase):
		def test_root(self):
				response = self.app.test_client().get('/')
				self.assertEqual(response.status_code, 200)
				self.assert_template_used('index.html')

		def test_media(self):
				response = self.app.test_client().get('/gostuvanja')
				self.assertEqual(response.status_code, 200)
				self.assert_template_used('gostuvanja.html')
