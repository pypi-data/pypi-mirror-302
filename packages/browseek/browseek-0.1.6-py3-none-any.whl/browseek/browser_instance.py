import asyncio
from .driver_router import DriverRouter

class BrowserInstance:
    def __init__(self, browser_type: str, options: dict = None):
        self.browser_type = browser_type
        self.options = options
        self.driver_router: DriverRouter = None

    async def launch(self):
        self.driver_router = DriverRouter(self.browser_type)
        await self.driver_router.initialize(**(self.options or {}))

    async def close(self):
        if self.driver_router:
            await self.driver_router.close()

    async def execute(self, url: str, func):
        await self.driver_router.goto(url)
        result = await func(self.driver_router.driver)
        return result

    def is_available(self):
        return self.driver_router is not None and self.driver_router.driver is not None

    @property
    def driver(self):
        return self.driver_router.driver if self.driver_router else None
