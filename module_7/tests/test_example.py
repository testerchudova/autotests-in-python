from time import sleep
import re
import allure
from random import uniform
from module_7.src.Utils.сhecking_elements import *  # noqa
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
            with allure.step(f'Получаем все названия задач на page {page_1}'):
                get_titles = web_driver_wait('div[class="js-navigation-container js-active-navigation-container"]>div')
                sleep(uniform(1, 5))
                list_titles = [text_contain(item, predicate) for item in get_titles.all()]
                test_page_ok = all(list_titles)

            with allure.step(f'Проверяем, что каждая из задач содержит в названии слово {predicate}'):
                assert test_page_ok, \
                    f'Один из элементов title, на странице {page_1} не содержит подстроки {predicate}'

            with allure.step(f'Переходим на page {page_1 + 1}'):
                page.locator('div.Box.mt-3+div a.next_page').click()
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
    def test_filling_out_form(seif, page, web_driver_wait):
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
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('В поле языка, на котором написан код, выбераем Python'):
            page.locator('//select[@id="search_language"]').select_option('Python')

        with allure.step(f'В поле количества звёзд у репозитория выберите > {number}'):
            page.locator('//input[@id="search_stars"]').fill(f">{number}")

        with allure.step('В поле с названием файла вводим environment.yml'):
            page.locator('//input[@id="search_filename"]').fill("environment.yml")

        with allure.step('Нажмаем на кнопку поиска'):
            page.locator('//div[@class="form-group flattened"]//button').click()

        page_1 = 1
        number /= 1000
        with allure.step(f'Проверяем, что в списке отображаются репозитории с количеством звёзд > {number}k'):
            while not is_element(page, 'span[class="next_page disabled"]') and (page_1 < 3):
                items_list = web_driver_wait('//a[@class = "Link--muted"]')
                test_page_ok = all([float(item.inner_text()[0:-1]) > number for item in items_list.all()])

                with allure.step(f'Количество звезд на page {page_1}, соответствует условию > {number}k'):
                    assert test_page_ok, f"Количество звезд не соответствует условию > {number}k"
                    page.locator('a.next_page').click()
                    sleep(uniform(4, 10))
                page_1 += 1

    @allure.title('Выбор онлайн-курсов по программированию от Skillbox')
    def test_course_selection(seif, web_driver_wait, page):
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
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Выбераем радио-баттон с названием «Профессия» в разделе «Тип обучения на платформе»'):
            page.locator('input[value="profession"]+span').click()

        with allure.step('В тематике выбераем чекбокс "Android" и "Backend-разработка"'):
            page.locator('//span[span[contains(text(),"Android")]]').click()
            page.locator('//span[span[contains(text(),"Backend-разработка")]]').click()

        with allure.step('Указываем в поле «Длительность» диапазон от 6 до 12 месяцев (через движение мышки)'):
            butt_end = page.locator('div[aria-valuetext="24"]>button')
            butt_first = page.locator('div[aria-valuetext="1"]>button')

            moving_element(page, butt_first, [100, 0])
            moving_element(page, butt_end, [240, 0])

        with allure.step('Проверка, что в списке находятся ожидаемые курсы'):
            count_curses_text = web_driver_wait('div.courses-block__top>h2')
            butt_curse = web_driver_wait('button.courses-block__load')

            while not (butt_curse is None):
                butt_curse.click()
                sleep(1)
                butt_curse = web_driver_wait('button.courses-block__load', timeout=100)

            logging.info('Получаем список курсов')
            list_courses = page.locator('a.ui-product-card-main__wrap')
            list_courses_count = list_courses.count()
            count_curses = int(re.search(r'\.*(\d+)', count_curses_text.inner_text()).group())
            if list_courses_count != count_curses:
                raise Exception(
                    f'Количество найденых курсов "{list_courses_count}" '
                    f'не соответствует заявленным в строке "{count_curses_text.inner_text()}"')

            list_cour = ['разработ', 'android', 'developer']
            res = []

            for item_courses in list_courses.all():
                for item_cour in list_cour:
                    if item_cour in item_courses.inner_text().lower():
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

        with allure.step('Поиск столбца гистограммы'):
            logging.info("Поиск столбца гистограммы")

            graf = page.locator('section g.bar.mini:nth-of-type(15)')

        with allure.step('Перемещаем указатель мыши на столбец гистограммы'):
            logging.info("Перемещаем указатель мыши на столбец гистограммы")
            graf.hover()

        with allure.step('Проверяем, что в отображаемом тултипе находится ожидаемые значения'):
            logging.info("Проверяем, что в отображаемом тултипе находится ожидаемые значения")

            tultype = web_driver_wait('div.svg-tip > strong')
            tultype_text = '144'
            assert tultype.inner_text() in tultype_text, f"Текст в тултипе не содержит {tultype_text}"

        logging.info("Тест завершен успешно")
