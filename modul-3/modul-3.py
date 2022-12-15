<<<<<<< HEAD
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
=======
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as Firefox_options
path = "..\..\geckodriver-v0.31.0-win64\geckodriver.exe"

def run_script():
    options = Firefox_options()
    driver = Firefox(executable_path=path, options=options)
    driver.get("https://go.skillbox.ru/")
    # sleep(10)
    # driver.quit()

# Что нужно сделать
# Для сайта GitHub или Python напишите несколько разных CSS- и xPath-локаторов.
#
# Должны быть составлены следующие локаторы:
#
# иерархические (вложенность — три элемента);
# по атрибутам: класс, идентификатор, имя;
# по кастомным атрибутам: data-*;
# связка иерархического и атрибута (например, //div[@attr=””]);
# два разных локатора с поиском чайлда, парента и соседей (sibling и not-sibling);
# для xPath с использованием функций;
# для CSS с использованием псевдоселекторов.
# Вместе с локатором желательно оставить скриншот и ссылку на страницу, чтобы было проще проверять работу.












if __name__ == "__main__":
    run_script()
>>>>>>> 1dbf04d659192e42bac370d1a162e056efae74a3
