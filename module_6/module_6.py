from selenium.webdriver import Chrome, Remote, ChromeOptions
#from selenium.webdriver.chrome.options import ChromiumOptions as ChromeOptions
#import chromedriver_binary



def run_script():

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

    driver.get("https://selenium-python.readthedocs.io/locating-elements.html")
    driver.quit()
    pass

if __name__ == "__main__":
    run_script()