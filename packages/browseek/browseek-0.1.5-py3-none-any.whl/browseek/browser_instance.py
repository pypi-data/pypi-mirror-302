import asyncio
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

class BrowserInstance:
    def __init__(self, browser_type: str, options: dict = None):
        self.browser_type = browser_type
        self.options = options
        self._browser: Browser = None
        self._context: BrowserContext = None
        self._page: Page = None

    async def launch(self):
        playwright = await async_playwright().start()
        self._browser = await playwright[self.browser_type].launch(**(self.options or {}))
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()

    async def close(self):
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()

    async def execute(self, url: str, func):
        await self._page.goto(url)
        result = await func(self._page)
        return result

    def is_available(self):
        return self._browser is not None and self._context is not None and self._page is not None

    @property
    def browser(self):
        return self._browser

    @property
    def context(self):
        return self._context

    @property
    def page(self):
        return self._page
