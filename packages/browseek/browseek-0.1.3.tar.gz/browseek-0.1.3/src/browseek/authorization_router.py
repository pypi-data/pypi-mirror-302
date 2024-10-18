from typing import Dict, Any

class AuthorizationRouter:
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the AuthorizationRouter with optional configuration."""
        self.config = config or {}

    def basic_auth(self, username: str, password: str):
        """Set up basic authentication credentials."""
        self.config["auth"] = {
            "type": "basic",
            "username": username,
            "password": password
        }

    def session_auth(self, cookies: Dict[str, str]):
        """Set up session-based authentication using cookies."""
        self.config["auth"] = {
            "type": "session",
            "cookies": cookies
        }

    def oauth(self, access_token: str):
        """Set up OAuth authentication using an access token."""
        self.config["auth"] = {
            "type": "oauth",
            "access_token": access_token
        }

    def get_auth_config(self) -> Dict[str, Any]:
        """Get the current authentication configuration."""
        return self.config.get("auth", {})
