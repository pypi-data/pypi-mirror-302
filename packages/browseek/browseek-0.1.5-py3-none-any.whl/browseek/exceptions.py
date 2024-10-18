class BrowserNotAvailableError(Exception):
    """Raised when no browser instance is available to execute a task."""
    pass

class CaptchaError(Exception):
    """Raised when a CAPTCHA is encountered and needs to be solved."""
    def __init__(self, captcha_type, captcha_data):
        self.captcha_type = captcha_type
        self.captcha_data = captcha_data

class NetworkError(Exception):
    """Raised when a network error occurs during browser automation."""
    pass
