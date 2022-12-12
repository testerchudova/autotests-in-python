import math
import  numpy as np
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as Firefox_options
path = "..\..\geckodriver-v0.31.0-win64\geckodriver.exe"

def run_script():
    options = Firefox_options()
    driver = Firefox(executable_path=path, options=options)
    driver.get("https://go.skillbox.ru/")
    #driver.quit()



if __name__ == "__main__":
    run_script()
