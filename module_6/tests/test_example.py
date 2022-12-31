import logging

import allure
from time import sleep
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element_value
from selenium.common.exceptions import StaleElementReferenceException
from module_6.src.Utils.сhecking_elements import is_element
from module_6.src.actions.actions import *


class TestExample():

    # def test_find_title_bug(seif, selenium):
    #     """
    #     Кейс №1
    #     Шаги:
    #     1 Откройте страницу https://github.com/microsoft/vscode/issues.
    #     2 Введите в поиск фильтр in:title.
    #     3 Введите в поиск какие-то ключевые слова (слова, по которым можно найти любую из задач по названию). Например: bug.
    #     4 Нажмите на enter.
    #     5 Получите все названия задач.
    #     6 Проверьте, что каждая из задач содержит в названии слово bug (важно не учитывать регистр, то есть Bug и bug — это одно и то же).
    #     """
    #     line = "bug"
    #     driver = selenium
    #     page = driver.get("https://github.com/microsoft/vscode/issues")
    #     find_el = selenium.find_element(By.CSS_SELECTOR, "input#js-issues-search")
    #     find_el.clear()
    #     find_el.send_keys("in:title ")
    #     find_el.send_keys(line)
    #     ActionChains(selenium).key_down(Keys.ENTER).perform()
    #
    #     page = 1
    #
    #     while not is_element(By.CSS_SELECTOR, 'span[class="next_page disabled"]', selenium) and (page < 10):
    #         try:
    #             titles = WebDriverWait(selenium, timeout=3) \
    #                 .until(lambda d: d.find_elements(By.CSS_SELECTOR, \
    #                 'div[class="js-navigation-container js-active-navigation-container"]>div'))
    #             test_page_ok = all([item.text.upper().find(line.upper()) != -1 for item in titles])
    #             assert test_page_ok == True, f"'Один из элементов title, на странице {page} не содержит подстроки {line}"
    #             button_next = selenium.find_element(By.CSS_SELECTOR, 'a.next_page')
    #             button_next.click()
    #         except StaleElementReferenceException:
    #             continue
    #         page += 1
    #     pass
    #
    # def test_select_from_list(seif, selenium):
    #     """
    #     Кейс №2
    #     Шаги:
    #     1 Откройте страницу https://github.com/microsoft/vscode/issues.
    #     2 Нажмите на кнопку Author.
    #     3 Введите в поиск имя bpasero.
    #     4 Дождитесь появления в списке нужного автора
    #     4 Выберите в выпадающем списке элемент с названием
    #     5 Остановите выполнение автотеста и глазами проверьте, что все отображаемые задачи — от выбранного автора.
    #     6 Проверьте, что автор всех задач введён в поиск
    # """
    #     input_text = "bpasero"
    #     selenium.get("https://github.com/microsoft/vscode/issues")
    #     selenium.find_element(By.XPATH, '//summary[@title="Author"]').click()
    #     input_1 = selenium.find_element(By.XPATH, '//input[@id="author-filter-field"]')
    #     for simbol in input_text:
    #         input_1.send_keys(simbol)
    #         ActionChains(selenium).pause(uniform(0.2, 6)).perform()
    #
    #     item_list = WebDriverWait(selenium, timeout=6) \
    #         .until(lambda d: d.find_element(By.XPATH, '//button[@value="bpasero"]'))
    #     item_list.click()
    #
    #     is_text__value = text_to_be_present_in_element_value((By.CSS_SELECTOR, '#js-issues-search'), input_text)(
    #         selenium)
    #     assert is_text__value == True, f"В строке поиска отсутствует проверяемая сторка {input_text}"
    #
    # def test_filling_out_form(seif, selenium):
    #     """
    #     Кейс №3
    #     Шаги:
    #     1 Откройте страницу https://github.com/search/advanced.
    #     2 В поле языка, на котором написан код, выберите Python.
    #     3 В поле количества звёзд у репозитория выберите >20000.
    #     4 В поле с названием файла выберите environment.yml.
    #     5 Нажмите на кнопку поиска.
    #     6 Соберите информацию по всем репозиториям
    #     7 Проверьте, что в списке отображаются репозитории с количеством звёзд >20000
    #     """
    #     namber = 20000
    #     page = selenium.get("https://github.com/search/advanced")
    #     find_el_select_language = selenium.find_element(By.XPATH, '//select[@id="search_language"]')
    #     find_el_select_language.find_element(By.XPATH, '//option[@value="Python"]').click()
    #
    #     selenium.find_element(By.XPATH, '//input[@id="search_stars"]').send_keys(f">{namber}")
    #     selenium.find_element(By.XPATH, '//input[@id="search_filename"]').send_keys("environment.yml")
    #
    #     selenium.find_element(By.XPATH, '//div[@class="form-group flattened"]//button').click()
    #
    #     page = 1
    #     namber = namber / 1000
    #
    #     while not is_element(By.CSS_SELECTOR, 'span[class="next_page disabled"]', selenium):
    #         try:
    #             items_list = WebDriverWait(selenium, timeout=6) \
    #                 .until(lambda d: d.find_elements(By.XPATH, '//a[@class = "Link--muted"]'))
    #             test_page_ok = all([float(item.text[0:-1]) > namber for item in items_list])
    #             assert test_page_ok == True, f"Количество звезд не соответствует условию > {namber}k"
    #             selenium.find_element(By.CSS_SELECTOR, 'a.next_page').click()
    #             ActionChains(selenium).pause(uniform(4, 10)).perform()
    #
    #         except StaleElementReferenceException:
    #             continue
    #         page += 1
    #
    # def test_course_selection(seif, selenium):
    #     """
    #     Кейс №4
    #     Шаги:
    #     1 Перейдите на сайт «Онлайн-курсы по программированию от Skillbox».
    #     2 Выберите радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе».
    #     3 Укажите в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки).
    #     4 В тематике выберите любой из чекбоксов.
    #     5 Проверьте, что в списке находятся те курсы, которые вы ожидали.
    #     """
    #
    #     selenium.get("https://skillbox.ru/code/")
    #     selenium.find_element(By.CSS_SELECTOR, 'input[value="profession"]+span').click()
    #     selenium.find_element(By.XPATH, '//span[span[contains(text(),"Android")]]').click()
    #     selenium.find_element(By.XPATH, '//span[span[contains(text(),"Backend-разработка")]]').click()
    #     butt_end = selenium.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="24"]>button')
    #     butt_first = selenium.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="1"]>button')
    #
    #     moving_element(selenium, butt_first, [50, 0])
    #     moving_element(selenium, butt_end, [-60, 0])
    #
    #     list_courses = selenium.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')
    #     second = 6
    #     if is_element(By.CSS_SELECTOR, 'button.courses-block__load', selenium):
    #         ActionChains(selenium).pause(1).perform()
    #         selenium.find_element(By.CSS_SELECTOR, 'button.courses-block__load').click()
    #
    #         for time_1 in range(1, second * 2 + 1):
    #             list_courses_2 = selenium.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')
    #
    #             if len(list_courses_2) == len(list_courses):
    #                 ActionChains(selenium).pause(.5).perform()
    #             else:
    #                 list_courses = list_courses_2
    #                 break
    #
    #             if time_1 == second * 2:
    #                 raise Exception("Время истекло")
    #
    #     list_cour = ['разработ', 'android', 'developer']
    #     res = []
    #
    #     for item_courses in list_courses:
    #         for item_cour in list_cour:
    #             if item_cour in item_courses.text.lower():
    #                 res_loc = True
    #                 break
    #             res_loc = False
    #         res += [res_loc]
    #
    #     assert all(res) == True, f"Не все во всех карточках содержится хотябы одно из слов {list_cour}"


    @allure.step("Проверка что в отображаемом тултипе находится ожидаемые вами значения")
    def test_hover(seif, selenium):
        """
        Кейс №5
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/graphs/commit-activity.
        2 Наведите мышку на график.
        3 Проверьте, что в отображаемом тултипе находится ожидаемые вами значения.
        """
        logging.info("Запускаем страницу browser, URL https://github.com/microsoft/vscode/graphs/commit-activity")
        selenium.get("https://github.com/microsoft/vscode/graphs/commit-activity")
        sleep(1)

        graf = selenium.find_element(By.CSS_SELECTOR, 'section g:nth-of-type(15)')

        move_to_element(selenium, graf)

        # ActionChains(selenium) \
        #     .move_to_element(graf) \
        #     .perform()

        tultype = WebDriverWait(selenium, timeout=6) \
            .until(lambda d: d.find_element(By.CSS_SELECTOR, 'div.svg-tip > strong'))
        tultype_text = '287'
        assert tultype.text == tultype_text, f"Текст в тултипе не содержит {tultype_text}"

        logging.info("Тест завершен успешно")


"""
@allure.step("Проверка заголовка страниц")
def check_title(driver, title):
    assert driver.title == title


class TestExample:
    def test_example(self, selenium):
        
        selenium.get("https://selenium-python.readthedocs.io/locating-elements.html")
        check_title(selenium, '4. Locating Elements — Selenium Python Bindings 2 documentation')
        pass


    def test_example_2(self, selenium):
        
        selenium.get("https://www.ivi.ru/watch/132291")
        check_title(selenium, '4. Locating Elements — Selenium Python Bindings 2 documentation')


    def test_example2(self):
        print("script запущен")
        
"""
