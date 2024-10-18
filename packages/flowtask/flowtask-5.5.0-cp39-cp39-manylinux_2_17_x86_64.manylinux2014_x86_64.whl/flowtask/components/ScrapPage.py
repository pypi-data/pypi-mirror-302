"""
Scrapping a Web Page Using Selenium + ChromeDriver + BeautifulSoup.
"""
import asyncio
from collections.abc import Callable
import time
from pathlib import Path, PurePath
from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from lxml import html, etree
# Selenium Support:
from webdriver_manager.chrome import ChromeDriverManager
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from navconfig.logging import logging
from navconfig import BASE_DIR
# Internals
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported
)
from .abstract import FlowComponent
from .interfaces.http import HTTPService
from ..conf import (
    ### Oxylabs Proxy Support for Selenium
    OXYLABS_USERNAME,
    OXYLABS_PASSWORD,
    OXYLABS_ENDPOINT
)


logging.getLogger(name='selenium.webdriver').setLevel(logging.WARNING)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)
logging.getLogger(name='seleniumwire').setLevel(logging.WARNING)


class ScrapPage(FlowComponent, HTTPService):
    """ScrapPage.
        Scrapping a Web Page using Selenium.
    """
    chrome_options = [
        "--headless=new",
        "--enable-automation",
        "--lang=en",
        "--disable-extensions",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-features=NetworkService",
        "--disable-dev-shm-usage",
        "--disable-features=VizDisplayCompositor",
        "--disable-features=IsolateOrigins",
        "--ignore-certificate-errors-spki-list",
        "--ignore-ssl-errors"
    ]

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.url: str = kwargs.get("url", None)
        self.rotate_ua: bool = True
        kwargs['rotate_ua'] = True  # Forcing UA Rotation.
        # Fix the Headers for Scrapping:
        self.headers: dict = {
            "Host": self.extract_host(self.url),
            "Referer": self.url,
            "X-Requested-With": "XMLHttpRequest",
            "TE": "trailers",
        }
        # Configure Cookies:
        self.cookies: dict = kwargs.pop('cookies', {})
        self._driver: Callable = None
        self._wait: WebDriverWait = None
        self.use_selenium: bool = kwargs.pop(
            "use_selenium",
            False
        )
        # Accept Cookies is a tuple with button for accepting cookies.
        self.accept_cookies: tuple = kwargs.pop('accept_cookies', None)
        self.default_tag: str = kwargs.pop('default_tag', 'body')
        self.accept_is_clickable: bool = kwargs.pop('accept_is_clickable', False)
        self.timeout: int = kwargs.pop('timeout', 60)
        self.wait_until: tuple = kwargs.pop('wait_until', None)
        self.inner_tag: tuple = kwargs.pop('inner_tag', None)
        # URL Function: generate the URL based on a function:
        self.url_function: str = kwargs.pop('url_function', None)
        # Return the Driver (avoid closing the Driver at the end of the process).
        self.return_driver: bool = kwargs.pop('return_driver', False)
        super(ScrapPage, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # Selenium Options:
        self._options = Options()

    def extract_host(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def get_soup(self, content: str, parser: str = 'html.parser'):
        """Get a BeautifulSoup Object."""
        return BeautifulSoup(content, parser)

    def get_etree(self, content: str) -> tuple:
        try:
            x = etree.fromstring(content)
        except etree.XMLSyntaxError:
            x = None
        try:
            h = html.fromstring(content)
        except etree.XMLSyntaxError:
            h = None
        return x, h

    def check_by_attribute(self, attribute: tuple):
        el = attribute[0]
        value = attribute[1]
        new_attr = None
        if el == 'id':
            new_attr = (By.ID, value)
        elif el in ('class', 'class name'):
            new_attr = (By.CLASS_NAME, value)
        elif el == 'name':
            new_attr = (By.NAME, value)
        elif el == 'xpath':
            new_attr = (By.XPATH, value)
        elif el == 'css':
            new_attr = (By.CSS_SELECTOR, value)
        elif el in ('tag', 'tag name', 'tagname', 'tag_name'):
            new_attr = (By.TAG_NAME, value)
        else:
            raise NotSupported(
                f"Attribute {el} is not supported."
            )
        return new_attr

    async def start(self, **kwargs) -> bool:
        await super(ScrapPage, self).start(**kwargs)
        # Check the Accept Cookies:
        if self.accept_cookies:
            if not isinstance(self.accept_cookies, tuple):
                raise NotSupported(
                    "Accept Cookies must be a Tuple with the Button to Accept Cookies."
                )
            self.accept_cookies = self.check_by_attribute(self.accept_cookies)
        self.inner_tag = self.check_by_attribute(self.inner_tag)
        if hasattr(self, 'screenshot'):
            try:
                self.screenshot['portion'] = self.check_by_attribute(self.screenshot['portion'])
            except (KeyError, ValueError):
                pass
        if self.use_selenium is True:
            # Add UA to Headers:
            self._options.add_argument(f"user-agent={self._ua}")
            proxies = None
            if self.use_proxy is True:
                if self._free_proxy is False:
                    proxies = self.proxy_selenium(
                        OXYLABS_USERNAME, OXYLABS_PASSWORD, OXYLABS_ENDPOINT
                    )
                else:
                    proxy = await self.get_proxies()
                    self._options.add_argument(f"--proxy-server={proxy}")
            for option in self.chrome_options:
                self._options.add_argument(option)
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self._options,
                seleniumwire_options=proxies
            )
            self._wait = WebDriverWait(self._driver, self.timeout)
        # Generate a URL based on a URL Function:
        if self.url_function:
            fn = getattr(self, self.url_function, None)
            if fn:
                self.url = await fn()
        return True

    async def close(self, **kwargs) -> bool:
        if self.use_selenium is True:
            if self.return_driver is False:
                self._driver.quit()
        return True

    async def run_http(self):
        """Run the Scrapping Tool Using HTTPx."""
        result, error = await self.session(
            url=self.url,
            method=self.method,
            headers=self.headers,
            cookies=self.cookies,
            follow_redirects=True,
            use_proxy=self.use_proxy
        )
        if error:
            raise ComponentError(
                f"Error running Scrapping Tool: {error}"
            )
        if not result:
            raise DataNotFound(
                f"No content on URL {self.url}"
            )
        return result

    def _execute_scroll(self):
        """
        Execute JavaScript to scroll to the bottom of the page.
        """
        # Scroll to the bottom and back to the top
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Give some time for content to load
        self._driver.execute_script("window.scrollTo(0, 0);")

    def save_screenshot(self, filename: str) -> None:
        """Save the Screenshot."""
        original_size = self._driver.get_window_size()
        width = self._driver.execute_script(
            'return document.body.parentNode.scrollWidth'
        )
        height = self._driver.execute_script(
            'return document.body.parentNode.scrollHeight'
        )
        if not width:
            width = 1920
        if not height:
            height = 1080
        self._driver.set_window_size(width, height)
        self._execute_scroll()

        # Ensure the page is fully loaded after resizing
        self._wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # Wait for specific elements to load
        if self.wait_until:
            WebDriverWait(self._driver, 20).until(
                EC.presence_of_all_elements_located(
                    self.wait_until
                )
            )
        if 'portion' in self.screenshot:
            # Take a screenshot of a portion of the page
            self._driver.find_element(*self.screenshot['portion']).screenshot(filename)
        else:
            # Take a full-page screenshot
            self._driver.save_screenshot(filename)
        # resize to the Original Size:
        self._driver.set_window_size(
            original_size['width'],
            original_size['height']
        )

    def proxy_selenium(self, user: str, password: str, endpoint: str) -> dict:
        wire_options = {
            "proxy": {
                "http": f"http://{user}:{password}@{endpoint}",
                "https": f"https://{user}:{password}@{endpoint}",
                # "socks5": f"https://{user}:{password}@{endpoint}",
            }
        }
        return wire_options

    async def get_page_selenium(
        self,
        url: str,
        cookies: Optional[dict] = None,
    ):
        """get_page_selenium.

        Get one page using Selenium.
        """
        try:
            self._driver.get(url)
            if cookies:
                # Add the cookies
                for cookie_name, cookie_value in cookies.items():
                    self._driver.add_cookie({'name': cookie_name, 'value': cookie_value})
                    # Refresh the page to apply the cookies
                    self._driver.refresh()
            # Ensure the page is fully loaded before attempting to click
            self._wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            # Wait for specific elements to load (replace with your actual elements)
            if self.wait_until:
                WebDriverWait(self._driver, 20).until(
                    EC.presence_of_all_elements_located(
                        self.wait_until
                    )
                )
            else:
                # Wait for the tag to appear in the page.
                self._wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, self.default_tag)
                    )
                )
            # Accept Cookies if enabled.
            if self.accept_cookies:
                # Wait for the button to appear and click it.
                try:
                    # Wait for the "Ok" button to be clickable and then click it
                    if self.accept_is_clickable is True:
                        accept_button = self._wait.until(
                            EC.element_to_be_clickable(self.accept_cookies)
                        )
                        accept_button.click()
                    else:
                        accept_button = self._wait.until(
                            EC.presence_of_element_located(
                                self.accept_cookies
                            )
                        )
                    self._driver.execute_script("arguments[0].click();", accept_button)
                except TimeoutException:
                    self._logger.warning(
                        'Accept Cookies Button not found'
                    )
            # Execute an scroll of the page:
            self._execute_scroll()
        except TimeoutException:
            raise ComponentError(
                f"Timeout Error on URL {self.url}"
            )
        except Exception as exc:
            raise ComponentError(
                f"Error running Scrapping Tool: {exc}"
            )

    async def run_selenium(self):
        """Run the Scrapping Tool Using Selenium."""
        try:
            await self.get_page_selenium(self.url, self.cookies)
            file = None
            content = None
            if self.inner_tag:
                content = self._driver.find_element(*self.inner_tag).get_attribute('innerHTML')
            else:
                content = self._driver.page_source
            if hasattr(self, 'screenshot'):
                # capture an screenshot from the page and save it (and returning as binary as well)
                filename = self.screenshot.get('filename', 'screenshot.png')
                directory = Path(self.screenshot.get(
                    'directory', BASE_DIR.joinpath('static', 'images', 'screenshots')
                ))
                if not directory.is_absolute():
                    directory = BASE_DIR.joinpath('static', 'images', directory)
                if directory.exists() is False:
                    directory.mkdir(parents=True, exist_ok=True)
                # Take the screenshot
                file = directory.joinpath(filename)
                self.save_screenshot(str(file))
            # Return the content of the page.
            return content, file
        except TimeoutException:
            raise ComponentError(
                f"Timeout Error on URL {self.url}"
            )
        except Exception as exc:
            raise ComponentError(
                f"Error running Scrapping Tool: {exc}"
            )

    def _build_result_content(self, content: str, screenshot: PurePath) -> dict:
        """Build the Result Content."""
        soup = self.get_soup(content)
        _xml, _html = self.get_etree(content)
        return {
            "raw": content,
            "soup": soup,
            "html": _html,
            "xml": _xml,
            "screenshot": screenshot
        }

    async def run(self):
        """Run the Scrapping Tool."""
        self._result = None
        screenshot = None
        try:
            if self.use_selenium is True:
                content, screenshot = await self.run_selenium()
            else:
                content = await self.run_http()
            if not content:
                raise DataNotFound(
                    f"No content on URL {self.url}"
                )
        except ComponentError:
            raise
        except Exception as exc:
            raise ComponentError(
                f"Error running Scrapping Tool: {exc}"
            )
        if self.return_driver is True:
            self._result = self._driver
        else:
            self._result = self._build_result_content(content, screenshot)
        return self._result
