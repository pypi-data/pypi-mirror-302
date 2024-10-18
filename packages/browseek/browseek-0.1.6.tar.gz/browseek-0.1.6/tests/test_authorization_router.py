import unittest

from browseek import AuthorizationRouter

class TestAuthorizationRouter(unittest.TestCase):
    def setUp(self):
        self.router = AuthorizationRouter()

    def test_basic_auth(self):
        self.router.basic_auth("username", "password")
        auth_config = self.router.get_auth_config()
        self.assertEqual(auth_config["type"], "basic")
        self.assertEqual(auth_config["username"], "username")
        self.assertEqual(auth_config["password"], "password")

    def test_session_auth(self):
        cookies = {"session_id": "abc123"}
        self.router.session_auth(cookies)
        auth_config = self.router.get_auth_config()
        self.assertEqual(auth_config["type"], "session")
        self.assertEqual(auth_config["cookies"], cookies)

    def test_oauth(self):
        access_token = "xyz789"
        self.router.oauth(access_token)
        auth_config = self.router.get_auth_config()
        self.assertEqual(auth_config["type"], "oauth")
        self.assertEqual(auth_config["access_token"], access_token)

if __name__ == '__main__':
    unittest.main()
