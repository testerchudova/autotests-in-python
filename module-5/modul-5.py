from time import sleep
from random import uniform
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options as Firefox_options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element_value
from selenium.common.exceptions import InvalidSessionIdException, StaleElementReferenceException
from pathlib import Path
current_path = Path(__file__)
driver_path = current_path.parent.parent.joinpath("geckodriver-v0.31.0-win64", "geckodriver.exe")


class Tester():
    options = Firefox_options()
    options.page_load_strategy = "normal"
    driver = Firefox(executable_path=driver_path, options=options)
    
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
        4 Дождитесь появления в списке нужного автора
        4 Выберите в выпадающем списке элемент с названием
        5 Остановите выполнение автотеста и глазами проверьте, что все отображаемые задачи — от выбранного автора.
        6 Проверьте, что автор всех задач введён в поиск
    """
        input_text = "bpasero"
        Tester.driver.get("https://github.com/microsoft/vscode/issues")
        Tester.driver.find_element(By.XPATH, '//summary[@title="Author"]').click()
        input_1 = Tester.driver.find_element(By.XPATH, '//input[@id="author-filter-field"]')
        for simbol in input_text:
            input_1.send_keys(simbol)
            ActionChains(Tester.driver).pause(uniform(0.2, 6)).perform()
            


        item_list = WebDriverWait(Tester.driver, timeout=6) \
            .until(lambda d: d.find_element(By.XPATH, '//button[@value="bpasero"]'))
        item_list.click()

        is_text__value = text_to_be_present_in_element_value((By.CSS_SELECTOR, '#js-issues-search'), input_text)(Tester.driver)
        assert is_text__value == True, f"В строке поиска отсутствует проверяемая сторка {input_text}"

        print("Тест завершен успешно")


        pass

    def test_filling_out_form(seif):
        """
        Кейс №3
        Шаги:
        1 Откройте страницу https://github.com/search/advanced.
        2 В поле языка, на котором написан код, выберите Python.
        3 В поле количества звёзд у репозитория выберите >20000.
        4 В поле с названием файла выберите environment.yml.
        5 Нажмите на кнопку поиска.
        6 Соберите информацию по всем репозиториям
        7 Проверьте, что в списке отображаются репозитории с количеством звёзд >20000
        """
        namber = 20000
        page = Tester.driver.get("https://github.com/search/advanced")
        find_el_select_language = Tester.driver.find_element(By.XPATH, '//select[@id="search_language"]')
        find_el_select_language.find_element(By.XPATH, '//option[@value="Python"]').click()
        

        Tester.driver.find_element(By.XPATH, '//input[@id="search_stars"]').send_keys(f">{namber}")
        Tester.driver.find_element(By.XPATH, '//input[@id="search_filename"]').send_keys("environment.yml")       
        
        Tester.driver.find_element(By.XPATH, '//div[@class="form-group flattened"]//button').click()

        
        
        page = 1
        namber = namber/1000        
        
        while not Tester.is_element(By.CSS_SELECTOR, 'span[class="next_page disabled"]'):
            try:                
                items_list = WebDriverWait(Tester.driver, timeout=6) \
                    .until(lambda d: d.find_elements(By.XPATH, '//a[@class = "Link--muted"]'))
                test_page_ok = all([float(item.text[0:-1]) > namber for item in items_list])                
                assert test_page_ok == True, f"Количество звезд не соответствует условию > {namber}k"                
                Tester.driver.find_element(By.CSS_SELECTOR, 'a.next_page').click()
                ActionChains(Tester.driver).pause(uniform(4, 10)).perform()
                
            except StaleElementReferenceException:
                continue
            page += 1
        
        print("Тест завершен успешно.")


        pass
    
    
   
   
   
    def test_course_selection(seif):
        """
        Кейс №4
        Шаги:
        1 Перейдите на сайт «Онлайн-курсы по программированию от Skillbox».
        2 Выберите радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе».
        3 Укажите в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки).
        4 В тематике выберите любой из чекбоксов.
        5 Проверьте, что в списке находятся те курсы, которые вы ожидали. 
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

        list_courses = Tester.driver.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')
        second = 6
        if Tester.is_element(By.CSS_SELECTOR,'button.courses-block__load'):
            ActionChains(Tester.driver).pause(1).perform()
            Tester.driver.find_element(By.CSS_SELECTOR, 'button.courses-block__load').click() 

            for time_1 in range(1, second*2 + 1):
                list_courses_2 = Tester.driver.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')
                
                if len(list_courses_2) == len(list_courses):
                    ActionChains(Tester.driver).pause(.5).perform()
                else:
                    list_courses = list_courses_2
                    break

                if time_1 == second*2:
                    raise "Время истекло"



        list_cour = ['разработ', 'android', 'developer']    
        res = []

        for item_courses in list_courses:
            for item_cour in list_cour:                    
                if item_cour in item_courses.text.lower():
                    res_loc = True
                    break
                res_loc = False                
            res += [res_loc]

        assert all(res) == True, f"Не все во всех карточках содержится хотябы одно из слов {list_cour}"

        print("Тест завершен успешно.")

        pass

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
    # tester.test_find_title_bug()
    # tester.test_select_from_list()
    #tester.test_filling_out_form()
    #tester.test_course_selection()
    tester.test_hover()

