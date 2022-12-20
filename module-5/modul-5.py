from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as Firefox_options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import InvalidSessionIdException, StaleElementReferenceException
path = "..\.\geckodriver-v0.31.0-win64\geckodriver.exe"

class Tester():
    options = Firefox_options()
    options.page_load_strategy = "normal"
    driver = Firefox(executable_path=path, options=options)
    
    @classmethod
    def is_element(cls, common_by, selector):
        is_element = len(Tester.driver.find_elements(common_by, selector)) > 0
        return is_element

    def test_find_title_bug(seif):
        """
        Кейс №1
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/issues.
        2 Введите в поиск фильтр in:title.
        3 Введите в поиск какие-то ключевые слова (слова, по которым можно найти любую из задач по названию). Например: bug.
        4 Нажмите на enter.
        5 Получите все названия задач.
        6 Проверьте, что каждая из задач содержит в названии слово bug (важно не учитывать регистр, то есть Bug и bug — это одно и то же).
        """
        line = "bug"
        driver = Tester.driver  
        page = driver.get("https://github.com/microsoft/vscode/issues")
        find_el = Tester.driver.find_element(By.CSS_SELECTOR, "input#js-issues-search")
        find_el.clear()
        find_el.send_keys("in:title ")
        find_el.send_keys(line)
        actions = ActionChains(Tester.driver).key_down(Keys.ENTER).perform()

        
        page = 1
        
        while not Tester.is_element(By.CSS_SELECTOR, 'span[class="next_page disabled"]') and (page < 10):
            try:
                titles = WebDriverWait(Tester.driver, timeout=3)\
                        .until(lambda d: d.find_elements(By.CSS_SELECTOR, 'div[class="js-navigation-container js-active-navigation-container"]>div'))
                test_page_ok = all([item.text.upper().find(line.upper()) != -1 for item in titles])                
                assert test_page_ok == True, f"'Один из элементов title, на странице {page} не содержит подстроки {line}"                
                button_next = Tester.driver.find_element(By.CSS_SELECTOR, 'a.next_page')
                button_next.click()  
            except StaleElementReferenceException:
                continue
            page += 1
        
        print("Тест завершен успешно.")



        pass




    
    def test_select_from_list(seif):
        """
        Кейс №2
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/issues.
        2 Нажмите на кнопку Author.
        3 Введите в поиск имя bpasero.
        4 Выберите в выпадающем списке элемент с названием
        5 Остановите выполнение автотеста и глазами проверьте, что все отображаемые задачи — от выбранного автора.
  https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.action_chains.html#selenium.webdriver.common.action_chains.ActionChains.move_to_element
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
        

        Tester.driver.find_element(By.XPATH, '//input[@id="search_stars"]').send_keys(">20000")
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

    def test_hover(seif):
        """
        Кейс №5
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/graphs/commit-activity.
        2 Наведите мышку на график.
        3 Проверьте, что мышка навелась корректно.  
        """
        
        page = Tester.driver.get("https://github.com/microsoft/vscode/graphs/commit-activity")
        sleep(1)

        graf = find_el_select_language = Tester.driver.find_element(By.CSS_SELECTOR, 'section g:nth-of-type(15)')

        ActionChains(Tester.driver)\
            .move_to_element(graf)\
            .perform()

       



if __name__ == "__main__":
    
    tester = Tester()
    tester.test_find_title_bug()
    # tester.test_select_from_list()
    # tester.test_filling_out_form()
    #tester.test_course_selection()
    #tester.test_hover()

