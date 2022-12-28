# -*- coding: utf-8 -*-
from selenium.webdriver import Remote
import pytest

@pytest.fixture()
def set_up_browser():
    capabilities = {
        "browserName": "chrome",
        "browserVersion": "108.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False,
            "sessionTimeout": "2h"
        }
    }
    driver = Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities=capabilities)

    yield driver
    #driver.quit()

class TestExample:
    def test_example(self, set_up_browser):
        driver = set_up_browser
        driver.get("https://selenium-python.readthedocs.io/locating-elements.html")
        pass


    # def test_example(self):
    #     print("script запущен")
    #
    def test_example2(self):
        print("script запущен")
