import math
import pytest
import  numpy as np
from selenium.webdriver import Firefox, Chrome, Remote
from selenium.webdriver.firefox.options import Options as Firefox_options
from selenium.webdriver.chrome.options import Options as Chrome_options
import chromedriver_binary
path = "..\..\geckodriver-v0.31.0-win64\geckodriver.exe"

def run_script():
    # options = Firefox_options()
    # driver = Firefox(executable_path=path, options=options)
    # driver.get("https://go.skillbox.ru/")
    #driver.quit()
    # driver = Remote(desired_capabilities={"browserName":"firefox", "browserVersion":"latest"}, command_executor="http://127.0.0.1:4444/wd/hub")
    # driver.get("https://go.skillbox.ru/")

    options = Chrome_options()
    #options.headless = True
    driver = Chrome(options=options)
    driver.get("https://go.skillbox.ru/")





if __name__ == "__main__":
    run_script()
