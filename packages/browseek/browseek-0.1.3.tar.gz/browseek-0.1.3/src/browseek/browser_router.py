from typing import Dict, Any, List, Tuple, Callable
from . import MAX_CONCURRENT_BROWSERS, DEFAULT_TIMEOUT, RETRY_ATTEMPTS

from .browser_instance import BrowserInstance
from .request_interceptor import RequestInterceptor
from .device_profile import DeviceProfile
from .network_config import NetworkConfig
from .captcha_solver import CaptchaSolver
from .exceptions import BrowserNotAvailableError, CaptchaError, NetworkError

class BrowserRouter:
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the BrowserRouter with optional configuration."""
        self.config = config or {}
        self.max_concurrent_browsers = self.config.get("max_concurrent_browsers", MAX_CONCURRENT_BROWSERS)
        self.default_timeout = self.config.get("default_timeout", DEFAULT_TIMEOUT)
        self.retry_attempts = self.config.get("retry_attempts", RETRY_ATTEMPTS)
        self.browsers = []
        self.request_interceptor = None
        self.device_profile = None
        self.network_config = None
        self.captcha_solver = None

    def add_browser(self, browser_type: str, count: int = 1, options: Dict[str, Any] = None):
        """Add browser instances to the pool."""
        for _ in range(count):
            browser = BrowserInstance(browser_type, options)
            self.browsers.append(browser)

    def set_request_interceptor(self, interceptor: RequestInterceptor):
        """Set a custom request interceptor for all managed browsers."""
        self.request_interceptor = interceptor

    def set_device_profile(self, profile: DeviceProfile):
        """Set a device profile for browser simulation."""
        self.device_profile = profile

    def set_network_config(self, config: NetworkConfig):
        """Set network configuration including VPN and speed limits."""
        self.network_config = config

    def execute(self, url: str, task: Callable) -> Any:
        """Execute a single task."""
        browser = self._get_available_browser()
        if not browser:
            raise BrowserNotAvailableError("No browser available to execute the task")

        try:
            browser.configure(self.request_interceptor, self.device_profile, self.network_config)
            result = task(browser)
            return result
        except CaptchaError as e:
            if self.captcha_solver:
                solution = self.captcha_solver.solve(e.captcha_type, e.captcha_data)
                browser.solve_captcha(solution)
                return self.execute(url, task)
            else:
                raise
        except NetworkError:
            # Retry or handle network errors
            raise
        finally:
            browser.cleanup()

    def execute_batch(self, tasks: List[Tuple[str, Callable]]) -> List[Any]:
        """Execute a batch of tasks in parallel."""
        results = []
        for url, task in tasks:
            result = self.execute(url, task)
            results.append(result)
        return results

    def _get_available_browser(self) -> BrowserInstance:
        for browser in self.browsers:
            if browser.is_available():
                return browser
        return None

    def close(self):
        """Close all browser instances and clean up resources."""
        for browser in self.browsers:
            browser.quit()
        self.browsers = []
