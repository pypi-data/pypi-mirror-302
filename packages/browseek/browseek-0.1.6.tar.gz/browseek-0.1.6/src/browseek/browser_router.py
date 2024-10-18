import asyncio
from typing import List
from .browser_instance import BrowserInstance

class BrowserRouter:
    def __init__(self):
        self.browser_instances: List[BrowserInstance] = []

    async def add_browser(self, browser_type: str, count: int = 1, options: dict = None):
        browser_instances = [BrowserInstance(browser_type, options=options) for _ in range(count)]
        for instance in browser_instances:
            await instance.launch()
        self.browser_instances.extend(browser_instances)

    async def remove_browser(self, browser_instance: BrowserInstance):
        await browser_instance.close()
        self.browser_instances.remove(browser_instance)

    async def close(self):
        for instance in self.browser_instances:
            await instance.close()
        self.browser_instances = []

    async def execute(self, url: str, func):
        browser = await self._get_available_browser()
        if browser:
            try:
                result = await browser.execute(url, func)
                return result
            finally:
                await self._release_browser(browser)
        else:
            raise Exception("No available browser instances")

    async def _get_available_browser(self) -> BrowserInstance:
        while True:
            for browser in self.browser_instances:
                if browser.is_available():
                    await self._acquire_browser(browser)
                    return browser
            await asyncio.sleep(0.1)

    async def _acquire_browser(self, browser: BrowserInstance):
        browser.is_available = lambda: False

    async def _release_browser(self, browser: BrowserInstance):
        browser.is_available = lambda: True
