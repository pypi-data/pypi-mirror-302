from typing import Dict, Any
from playwright.async_api import async_playwright
from . import PROXY_ENABLED, PROXY_ROTATE_ON_FAILURE

class BrowserInstance:
    def __init__(self, browser_type: str, options: Dict[str, Any] = None):
        """Initialize a browser instance."""
        self.browser_type = browser_type
        self.options = options or {}
        self.proxy_enabled = self.options.get("proxy_enabled", PROXY_ENABLED)
        self.proxy_rotate_on_failure = self.options.get("proxy_rotate_on_failure", PROXY_ROTATE_ON_FAILURE)
        self.browser = None
        self.context = None
        self.page = None

    async def _launch_browser(self):
        """Launch the browser instance."""
        playwright = await async_playwright().start()
        browser_type = getattr(playwright, self.browser_type)
        browser_options = self.options.get("browser_options", {})
        self.browser = await browser_type.launch(**browser_options)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def configure(self, request_interceptor, device_profile, network_config):
        """Configure the browser instance."""
        if request_interceptor:
            await self.context.route("**/*", request_interceptor.intercept)
        if device_profile:
            await self.context.set_viewport_size(device_profile.screen_size)
            await self.context.set_user_agent(device_profile.user_agent)
        if network_config:
            if network_config.vpn_config:
                await self.context.set_extra_http_headers({"X-VPN-Provider": network_config.vpn_config["provider"]})
            if network_config.speed_limit:
                await self.context.set_offline(True)
                await self.context.set_extra_http_headers({"X-Speed-Limit": str(network_config.speed_limit)})

    def is_available(self) -> bool:
        """Check if the browser instance is available for use."""
        return self.browser is not None and self.context is not None and self.page is not None

    async def solve_captcha(self, solution: str):
        """Solve CAPTCHA in the browser instance."""
        await self.page.type("#captcha-input", solution)
        await self.page.click("#captcha-submit")

    async def cleanup(self):
        """Clean up the browser instance after use."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()

    async def quit(self):
        """Quit the browser instance."""
        if self.browser:
            await self.browser.close()
