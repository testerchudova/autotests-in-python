from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as Firefox_options
path = "..\.\geckodriver-v0.31.0-win64\geckodriver.exe"
#path = "c:\Users\git\geckodriver-v0.31.0-win64\geckodriver.exe"
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

class Tester():
    options = Firefox_options()
    driver = Firefox(executable_path=path, options=options)

    def hierarchical_nesting(seif):
        """
        иерархические (вложенность — три элемента);     
        """
        driver = Tester.driver  
        page = driver.get("https://github.com/microsoft/vscode/issues")
        find_el = Tester.driver.find_element(By.CSS_SELECTOR, "input#js-issues-search")
        find_el.clear()
        find_el.send_keys("in:title ")
        find_el.send_keys("bug")
        actions = ActionChains(Tester.driver)
        actions.key_down(Keys.ENTER)
        actions.perform()

        #actions = ActionChains(driver)
        #actions.click(find_el)
        #actions.perform()



        pass






if __name__ == "__main__":
    
    tester = Tester()
    tester.hierarchical_nesting()
