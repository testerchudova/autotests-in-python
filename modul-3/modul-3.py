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

class Tester():
    options = Firefox_options()
    driver = Firefox(executable_path=path, options=options)

    def hierarchical_nesting(seif):
        """
        иерархические (вложенность — три элемента);     
        """        
        Tester.driver.get("https://go.skillbox.ru/")





if __name__ == "__main__":
    
    tester = Tester()
    tester.hierarchical_nesting()
