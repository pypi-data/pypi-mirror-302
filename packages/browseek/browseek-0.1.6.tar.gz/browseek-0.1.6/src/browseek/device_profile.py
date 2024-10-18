from typing import Tuple

class DeviceProfile:
    def __init__(self, user_agent: str, screen_size: Tuple[int, int], os: str, browser: str):
        """Initialize a device profile for simulation."""
        self.user_agent = user_agent
        self.screen_size = screen_size
        self.os = os
        self.browser = browser
