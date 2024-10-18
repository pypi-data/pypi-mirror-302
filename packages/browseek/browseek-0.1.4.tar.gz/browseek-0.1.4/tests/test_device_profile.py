import unittest

from browseek import DeviceProfile

class TestDeviceProfile(unittest.TestCase):
    def test_device_profile_initialization(self):
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        screen_size = (375, 812)
        os = "iOS"
        browser = "Safari"

        profile = DeviceProfile(user_agent, screen_size, os, browser)

        self.assertEqual(profile.user_agent, user_agent)
        self.assertEqual(profile.screen_size, screen_size)
        self.assertEqual(profile.os, os)
        self.assertEqual(profile.browser, browser)

if __name__ == '__main__':
    unittest.main()
