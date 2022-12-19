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

    def test_find_title_bug(seif):
        """
        Кейс №1
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/issues.
        2 Введите в поиск фильтр in:title.
        3 Введите в поиск какие-то ключевые слова (слова, по которым можно найти любую из задач по названию). Например: bug.
        4 Нажмите на enter.
        5 Остановите выполнение автотеста и глазами проверьте, что отображаются только те задачи, которые содержат слово bug.    
        """
        driver = Tester.driver  
        page = driver.get("https://github.com/microsoft/vscode/issues")
        find_el = Tester.driver.find_element(By.CSS_SELECTOR, "input#js-issues-search")
        find_el.clear()
        find_el.send_keys("in:title ")
        find_el.send_keys("bug")
        actions = ActionChains(Tester.driver).key_down(Keys.ENTER).perform()
    
    def test_select_from_list(seif):
        """
        Кейс №2
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/issues.
        2 Нажмите на кнопку Author.
        3 Введите в поиск имя bpasero.
        4 Выберите в выпадающем списке элемент с названием
        5 Остановите выполнение автотеста и глазами проверьте, что все отображаемые задачи — от выбранного автора.
  
        """
        
        page = Tester.driver.get("https://github.com/microsoft/vscode/issues")
        find_el_author = Tester.driver.find_element(By.XPATH, '//summary[@title="Author"]').click()
        find_el_input = Tester.driver.find_element(By.XPATH, '//input[@id="author-filter-field"]').send_keys("bpasero")
        ActionChains(Tester.driver).pause(1).perform()
        Tester.driver.find_element(By.XPATH, '//button[@value="bpasero"]').click()    

    def test_filling_out_form(seif):
        """
        Кейс №3
        Шаги:
        1 Откройте страницу https://github.com/search/advanced.
        2 В поле языка, на котором написан код, выберите Python.
        3 В поле количества звёзд у репозитория выберите >20000.
        4 В поле с названием файла выберите environment.yml.
        5 Нажмите на кнопку поиска.
        6 Остановите выполнение автотеста и глазами проверьте, что отображаются репозитории по выбранным критериям.  
        """
        
        page = Tester.driver.get("https://github.com/search/advanced")
        find_el_select_language = Tester.driver.find_element(By.XPATH, '//select[@id="search_language"]')
        find_el_select_language.find_element(By.XPATH, '//option[@value="Python"]').click()
        

        Tester.driver.find_element(By.XPATH, '//input[@id="search_stars"]').send_keys(">2000")
        Tester.driver.find_element(By.XPATH, '//input[@id="search_filename"]').send_keys("environment.yml")       
        
        Tester.driver.find_element(By.XPATH, '//div[@class="form-group flattened"]//button').click()
   
   
   
    def test_course_selection(seif):
        """
        Кейс №4
        Шаги:
        1 Перейдите на сайт «Онлайн-курсы по программированию от Skillbox».
        2 Выберите радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе».
        3 Укажите в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки).
        4 В тематике выберите любой из чекбоксов.
        5 Остановите выполнение автотеста и глазами проверьте, что отображаются правильные данные. 
        """
        
        page = Tester.driver.get("https://skillbox.ru/code/")
        Tester.driver.find_element(By.CSS_SELECTOR, 'input[value="profession"]+span').click()       
        Tester.driver.find_element(By.XPATH, '//span[span[contains(text(),"Android")]]').click()
        Tester.driver.find_element(By.XPATH, '//span[span[contains(text(),"Backend-разработка")]]').click()
        butt_end = Tester.driver.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="24"]>button')
        butt_first = Tester.driver.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="1"]>button')
        
        ActionChains(Tester.driver)\
            .click_and_hold(butt_first)\
            .move_by_offset(50, 0)\
            .release()\
            .perform()

        ActionChains(Tester.driver)\
            .click_and_hold(butt_end)\
            .move_by_offset(-60, 0)\
            .release()\
            .perform()


       






if __name__ == "__main__":
    
    tester = Tester()
    # tester.test_find_title_bug()
    # tester.test_select_from_list()
    # tester.test_filling_out_form()
    tester.test_course_selection()

