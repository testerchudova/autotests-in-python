import pytest
from playwright._impl._api_types import TimeoutError


@pytest.fixture
def web_driver_wait(page):
    def callback(selector, timeout=30000):
        try:
            page.wait_for_selector(selector, timeout=timeout)
            res = page.locator(selector)
        except TimeoutError:
            res = None
        return res
    return callback
