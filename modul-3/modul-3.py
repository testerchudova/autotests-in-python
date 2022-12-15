from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as Chrome_Options
import chromedriver_binary

print("Start")

def run_script():
    options = Chrome_Options()
    driver = Chrome(options=options)
    driver.get("https://github.com/testerchudova/autotests-in-python")
    driver.get("https://git-scm.com/download/win")
    #driver.quit()

#run_script()
options = Chrome_Options()
driver = Chrome(options=options)
driver.get("https://github.com/testerchudova/autotests-in-python")
driver.get("https://git-scm.com/download/win")
driver.get_screenshot_as_file(r"c:\Users\git")