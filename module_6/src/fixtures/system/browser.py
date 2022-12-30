from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as Chrome_options
import pytest



@pytest.fixture()
def selenium(pytestconfig):
    options = Chrome_options()
    options.page_load_strategy = "normal"

    capabilities = {
        "browserName": pytestconfig.getini("browser_name"),
        "browserVersion": pytestconfig.getini("browser_version"),
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False,
            "sessionTimeout": "2h"
        }
    }

    driver = Remote(command_executor=pytestconfig.getini("selenium_url"), desired_capabilities=capabilities, options=options)

    yield driver
    driver.quit()