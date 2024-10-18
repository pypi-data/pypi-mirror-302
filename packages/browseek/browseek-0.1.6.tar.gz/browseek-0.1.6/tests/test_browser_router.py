import os
import unittest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

from browseek import BrowserRouter, BrowserInstance

# Load environment variables from .env file
load_dotenv()

TEST_URL = os.getenv("TEST_URL")

class TestBrowserRouter(unittest.TestCase):
    def setUp(self):
        self.router = BrowserRouter()

    def test_add_browser(self):
        self.router.add_browser("chrome", count=2)
        self.assertEqual(len(self.router.browsers), 2)
        self.assertIsInstance(self.router.browsers[0], BrowserInstance)

    def test_execute_task(self):
        mock_browser = MagicMock(spec=BrowserInstance)
        mock_browser.is_available.return_value = True

        with patch.object(self.router, '_get_available_browser', return_value=mock_browser):
            def example_task(browser):
                return "Example Title"

            result = self.router.execute(TEST_URL, example_task)

        mock_browser.configure.assert_called_once()
        mock_browser.cleanup.assert_called_once()
        self.assertEqual(result, "Example Title")

    def test_execute_batch(self):
        mock_browser1 = MagicMock(spec=BrowserInstance)
        mock_browser1.is_available.return_value = True

        mock_browser2 = MagicMock(spec=BrowserInstance)
        mock_browser2.is_available.return_value = True

        with patch.object(self.router, '_get_available_browser', side_effect=[mock_browser1, mock_browser2]):
            def task1(browser):
                return "Example Title"

            def task2(browser):
                return TEST_URL

            tasks = [
                (TEST_URL, task1),
                (TEST_URL, task2)
            ]

            results = self.router.execute_batch(tasks)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "Example Title")
        self.assertEqual(results[1], TEST_URL)
        mock_browser1.configure.assert_called_once()
        mock_browser1.cleanup.assert_called_once()
        mock_browser2.configure.assert_called_once()
        mock_browser2.cleanup.assert_called_once()

    def test_close(self):
        mock_browser1 = MagicMock(spec=BrowserInstance)
        mock_browser2 = MagicMock(spec=BrowserInstance)
        self.router.browsers = [mock_browser1, mock_browser2]

        self.router.close()

        mock_browser1.quit.assert_called_once()
        mock_browser2.quit.assert_called_once()
        self.assertEqual(len(self.router.browsers), 0)

if __name__ == '__main__':
    unittest.main()
