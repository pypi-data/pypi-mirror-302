from typing import Union
from playwright.async_api import Page as PlaywrightPage
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from pyppeteer.page import Page as PuppeteerPage

class DriverRouter:
    def __init__(self, driver_type: str):
        self.driver_type = driver_type
        self.driver: Union[PlaywrightPage, SeleniumWebDriver, PuppeteerPage] = None

    async def initialize(self, **kwargs):
        if self.driver_type == "playwright":
            from playwright.async_api import async_playwright
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(**kwargs)
            self.driver = await browser.new_page()
        elif self.driver_type == "selenium":
            from selenium import webdriver
            self.driver = webdriver.Chrome(**kwargs)
        elif self.driver_type == "puppeteer":
            import asyncio
            from pyppeteer import launch
            browser = await launch(**kwargs)
            self.driver = await browser.newPage()
        else:
            raise ValueError(f"Unsupported driver type: {self.driver_type}")

    async def goto(self, url: str, **kwargs):
        if self.driver_type == "playwright":
            await self.driver.goto(url, **kwargs)
        elif self.driver_type == "selenium":
            self.driver.get(url)
        elif self.driver_type == "puppeteer":
            await self.driver.goto(url, **kwargs)

    async def close(self):
        if self.driver_type == "playwright":
            await self.driver.close()
        elif self.driver_type == "selenium":
            self.driver.quit()
        elif self.driver_type == "puppeteer":
            await self.driver.close()
