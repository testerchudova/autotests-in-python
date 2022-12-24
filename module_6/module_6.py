from selenium.webdriver import Chrome, Remote
from selenium.webdriver.chrome.options import ChromiumOptions as ChromeOptions
import chromedriver_binary



def run_script():
    # options = ChromeOptions()
    # driver = Chrome(options=options)
    # driver.get("https://selenium-python.readthedocs.io/locating-elements.html")

    driver = Remote(desired_capabilities={
        "browserName":"chrome",
        "browserVersion":"latest"
    }, command_executor="http://127.0.0.1")
    driver.get("https://selenium-python.readthedocs.io/locating-elements.html")

    pass

if __name__ == "__main__":
    run_script()