from selenium.webdriver import Remote
import logging
from selenium.webdriver.chrome.options import Options as Chrome_options
import pytest


@pytest.fixture()
def selenium(pytestconfig):

    options = Chrome_options()
    options.page_load_strategy = "normal"
    options.add_argument('--window-size=1920,1080')
    options.add_argument('----window-position=1530,-220')
    capabilities = {
        "browserName": pytestconfig.getini("browser_name"),
        "browserVersion": pytestconfig.getini("browser_version"),
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False,
            "sessionTimeout": "2h"
        }
    }
    logging.info("Браузер запустился")
    driver = Remote(command_executor=pytestconfig.getini("selenium_url"), desired_capabilities=capabilities,
                    options=options)

    yield driver
    driver.quit()
    logging.info("Браузер завершил сессию")
