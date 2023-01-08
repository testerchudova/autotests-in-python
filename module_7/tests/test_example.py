import logging
from time import sleep
from pprint import pprint
import allure
from random import uniform
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element_value
from selenium.common.exceptions import StaleElementReferenceException
from module_7.src.Utils.сhecking_elements import  *  # noqa
from module_7.src.actions.actions import *  # noqa



class TestExample():
    @allure.title('Поиск задач на github по заголовкам')
    def test_find_title_bug(seif, web_driver_wait, page):
        """
        Кейс №1
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/issues.
        2 Введите в поиск фильтр in:title.
        3 Введите в поиск какие-то ключевое слово bug (слова, по которым можно найти любую из задач по названию).
        4 Нажмите на enter.
        5 Получите все названия задач.
        6 Проверьте, что каждая из задач содержит в названии слово bug (важно не учитывать регистр,
        то есть Bug и bug — это одно и то же).
        """
        predicate = "bug"
        url = 'https://github.com/microsoft/vscode/issues'
        with allure.step(f'Открываем страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')
            with allure.step('Очищаем поле ввода и вводим in:title'):
                find_el = page.locator("input#js-issues-search")
                find_el.fill("in:title ")

            with allure.step(f'Вводим {predicate}'):
                page.keyboard.type(predicate)
            with allure.step('Нажимаем ENTER'):
                page.keyboard.press("Enter")

        page_1 = 1

        while not is_element(page, 'span[class="next_page disabled"]') and (page_1 < 3):
            try:
                with allure.step(f'Получаем все названия задач на page {page_1}'):

                    get_titles = web_driver_wait('div[class="js-navigation-container js-active-navigation-container"]>div')
                    sleep(1)
                    list_titles = [text_contain(item, predicate) for item in get_titles.all()]
                    test_page_ok = all(list_titles)

                with allure.step(f'Проверяем, что каждая из задач содержит в названии слово {predicate}'):
                    assert test_page_ok, \
                        f'Один из элементов title, на странице {page_1} не содержит подстроки {predicate}'

                with allure.step(f'Переходим на page {page_1 + 1}'):
                    page.locator('div.Box.mt-3+div a.next_page').click()
            except StaleElementReferenceException:
                continue

            page_1 += 1

    @allure.title('Выбор автора из выподающего списка')
    def test_select_from_list(seif, page, web_driver_wait):
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
        url = 'https://github.com/microsoft/vscode/issues'
        with allure.step(f'Открываем страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Нажмаем на кнопку Author'):
           page.locator('//summary[@title="Author"]').click()

        search_line = page.locator('#js-issues-search')
        input_1 = page.locator('//input[@id="author-filter-field"]')
        search_line.clear()
        with allure.step(f'Вводим в поиск имя {input_text}'):
            input_1.clear()
            for simbol in input_text:
                page.keyboard.type(simbol)
                sleep(0.3)

            get_button = web_driver_wait('//button[@value="bpasero"]')

        with allure.step('Выбераем в выпадающем списке элемент с названием'):
            get_button.click()

        with allure.step('Проверяем, что автор всех задач введён в поиск'):

            is_text_value = text_contain_input_value(search_line, input_text)
            assert is_text_value, f"В строке поиска отсутствует проверяемая сторка {input_text}"

    @allure.title('Проверка репозитория по количеству звезд > 20000')
    def test_filling_out_form(seif, selenium, web_driver_wait):
        """
        Кейс №3
        Шаги:
        1 Откройте страницу https://github.com/search/advanced.
        2 В поле языка, на котором написан код, выберите Python.
        3 В поле количества звёзд у репозитория выберите > 20000.
        4 В поле с названием файла выберите environment.yml.
        5 Нажмите на кнопку поиска.
        6 Соберите информацию по всем репозиториям
        7 Проверьте, что в списке отображаются репозитории с количеством звёзд >20000
        """
        number = 20000
        url = 'https://github.com/search/advanced'
        with allure.step(f'Открываем страницу {url}'):
            page = selenium.get(url)

        with allure.step('В поле языка, на котором написан код, выбераем Python'):
            find_el_select_language = selenium.find_element(By.XPATH, '//select[@id="search_language"]')
            find_el_select_language.find_element(By.XPATH, '//option[@value="Python"]').click()

        with allure.step(f'В поле количества звёзд у репозитория выберите > {number}'):
            selenium.find_element(By.XPATH, '//input[@id="search_stars"]').send_keys(f">{number}")

        with allure.step('В поле с названием файла вводим environment.yml'):
            selenium.find_element(By.XPATH, '//input[@id="search_filename"]').send_keys("environment.yml")

        with allure.step('Нажмаем на кнопку поиска'):
            selenium.find_element(By.XPATH, '//div[@class="form-group flattened"]//button').click()

        page = 1
        number /= 1000
        with allure.step(f'Проверяем, что в списке отображаются репозитории с количеством звёзд > {number}k'):
            while not is_element(By.CSS_SELECTOR, 'span[class="next_page disabled"]', selenium) and (page < 3):
                try:
                    items_list = web_driver_wait(By.XPATH, '//a[@class = "Link--muted"]', el="elements")
                    test_page_ok = all([float(item.text[0:-1]) > number for item in items_list])

                    with allure.step(f'Количество звезд на page {page}, соответствует условию > {number}k'):
                        assert test_page_ok, f"Количество звезд не соответствует условию > {number}k"
                        selenium.find_element(By.CSS_SELECTOR, 'a.next_page').click()
                        pause(selenium, timeout=uniform(4, 10))

                except StaleElementReferenceException:
                    continue
                page += 1

    @allure.title('Выбор онлайн-курсов по программированию от Skillbox')
    def test_course_selection(seif, selenium):
        """
        Кейс №4
        Шаги:
        1 Перейдите на сайт «Онлайн-курсы по программированию от Skillbox».
        2 Выберите радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе».
        3 Укажите в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки).
        4 В тематике выберите любой из чекбоксов.
        5 Проверьте, что в списке находятся те курсы, которые вы ожидали.
        """
        url = 'https://skillbox.ru/code/'
        with allure.step(f'Открываем страницу {url}'):
            selenium.get(url)

        with allure.step('Выбераем радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе»'):
            selenium.find_element(By.CSS_SELECTOR, 'input[value="profession"]+span').click()

        with allure.step('В тематике выбераем чекбокс "Android" и "Backend-разработка"'):
            selenium.find_element(By.XPATH, '//span[span[contains(text(),"Android")]]').click()
            selenium.find_element(By.XPATH, '//span[span[contains(text(),"Backend-разработка")]]').click()

        with allure.step('Указываем в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки)'):
            butt_end = selenium.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="24"]>button')
            butt_first = selenium.find_element(By.CSS_SELECTOR, 'div[aria-valuetext="1"]>button')

            moving_element(selenium, butt_first, [50, 0])
            moving_element(selenium, butt_end, [-60, 0])

        with allure.step('Проверка, что в списке находятся ожидаемые курсы'):

            list_courses = selenium.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')
            second = 6
            if is_element(By.CSS_SELECTOR, 'button.courses-block__load', selenium):
                pause(selenium, timeout=1)
                selenium.find_element(By.CSS_SELECTOR, 'button.courses-block__load').click()

                for time_1 in range(1, second * 2 + 1):
                    list_courses_2 = selenium.find_elements(By.CSS_SELECTOR, 'a.ui-product-card-main__wrap')

                    if len(list_courses_2) == len(list_courses):
                        pause(selenium, timeout=.5)
                    else:
                        list_courses = list_courses_2
                        break

                    if time_1 == second * 2:
                        raise Exception("Время истекло")

            list_cour = ['разработ', 'android', 'developer']
            res = []

            for item_courses in list_courses:
                for item_cour in list_cour:
                    if item_cour in item_courses.text.lower():
                        res_loc = True
                        break
                    res_loc = False
                res += [res_loc]

            assert all(res), f"Не все во всех карточках содержится хотябы одно из слов {list_cour}"

    @allure.title("Наведение указателя мыши на график и проверка ожидаемого значения в тултипе")
    def test_hover(seif, web_driver_wait, page):
        """
        Кейс №5
        Шаги:
        1 Откройте страницу https://github.com/microsoft/vscode/graphs/commit-activity.
        2 Наведите мышку на график.
        3 Проверьте, что в отображаемом тултипе находится ожидаемые вами значения.
        """
        url = 'https://github.com/microsoft/vscode/graphs/commit-activity'
        logging.info(f"Запускаем страницу browser, URL {url}")

        with allure.step(f'Открываем страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

            # pause(selenium, 2)

        with allure.step('Поиск столбца гистограммы'):
            logging.info("Поиск столбца гистограммы")

            graf = page.locator('section g.bar.mini:nth-of-type(15)')
            # graf = selenium.find_element(By.CSS_SELECTOR, 'section g:nth-of-type(15)')

        with allure.step('Перемещаем указатель мыши на столбец гистограммы'):
            logging.info("Перемещаем указатель мыши на столбец гистограммы")
            graf.hover()

        with allure.step('Проверяем, что в отображаемом тултипе находится ожидаемые значения'):
            logging.info("Проверяем, что в отображаемом тултипе находится ожидаемые значения")

            tultype = web_driver_wait('div.svg-tip > strong')
            tultype_text = '144'
            assert tultype.inner_text() in tultype_text, f"Текст в тултипе не содержит {tultype_text}"

        logging.info("Тест завершен успешно")
