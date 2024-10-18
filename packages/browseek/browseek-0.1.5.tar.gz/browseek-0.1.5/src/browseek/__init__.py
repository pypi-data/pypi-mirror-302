import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MAX_CONCURRENT_BROWSERS = int(os.getenv("MAX_CONCURRENT_BROWSERS", 5))
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 30))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "True").lower() == "true"
PROXY_ROTATE_ON_FAILURE = os.getenv("PROXY_ROTATE_ON_FAILURE", "True").lower() == "true"
DNS_OVER_HTTPS = os.getenv("DNS_OVER_HTTPS", "True").lower() == "true"
CAPTCHA_SERVICE = os.getenv("CAPTCHA_SERVICE", "2captcha")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")

from .browser_router import BrowserRouter
from .browser_instance import BrowserInstance
from .request_interceptor import RequestInterceptor
from .device_profile import DeviceProfile
from .network_config import NetworkConfig
from .captcha_solver import CaptchaSolver
from .exceptions import BrowserNotAvailableError, CaptchaError, NetworkError
from .authorization_router import AuthorizationRouter
