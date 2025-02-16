import unittest
from flask import Flask
from app.middlewares.auth import require_api_key
from unittest.mock import patch

class TestAuthMiddleware(unittest.TestCase):
    def setUp(self):
        """Set up a Flask test app with a test client."""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        @self.app.route("/protected")
        @require_api_key
        def protected_route():
            return "success"

    @patch("app.middlewares.auth.STATIC_API_KEY", "test_secret")  # Patch the static variable directly
    def test_api_key_auth_valid(self):
        """Test that a request with a valid API key passes."""
        response = self.client.get("/protected", headers={"X-API-Key": "test_secret"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "success")

    @patch("app.middlewares.auth.STATIC_API_KEY", "test_secret")  # Patch the static variable directly
    def test_api_key_auth_invalid(self):
        """Test that a request with an invalid API key fails."""
        response = self.client.get("/protected", headers={"X-API-Key": "wrong_key"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized", response.data.decode())

if __name__ == "__main__":
    unittest.main()
