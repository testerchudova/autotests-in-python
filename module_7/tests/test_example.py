from time import sleep
import re
import allure
from random import uniform

import pytest

from module_7.src.Utils.сhecking_elements import *  # noqa
from module_7.src.actions.actions import *  # noqa


class TestExample():

    @pytest.fixture
    def goto_to(page):
        def callback(url='http://pizzeria.skillbox.cc'):
            logging.info(f"Запускаем страницу browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

        return callback

    @pytest.fixture
    def authorization(page):
        def callback(nameuser='stepbystep', password_user='stepbystep23'):
            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                page.locator('li[id="menu-item-30"] a').click()

            with allure.step('Нажать на ссылку войти в хедере'):
                page.locator('div.login-woocommerce').click()

            with allure.step('Заполнить поля учетными данными пользователя'):
                page.locator('#username').fill(nameuser)
                page.locator('#password').fill(password_user)

            with allure.step('Нажать на кнопку войти'):
                page.locator('button[value="Войти"]').click()

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


    @allure.title("Поиск в Google Туроператор")
    def test_serch_google(seif, web_driver_wait, page):
        """
               Кейс №6
               Шаги:
               1 Откройте страницу https://www.google.com/webhp
               2 Ввести в поиск Туроператор.
               3 Нажмите на enter.
               4 Кликнуть по первой ссылке.

               """
        object_serch = 'Туроператор'
        url = 'https://www.google.com/webhp'
        logging.info(f"Запускаем страницу browser, URL {url}")
        with allure.step(f'Открыть страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step(f'Ввести в поисковую строку {object_serch}'):
            input_el_google = page.locator('input[class="gLFyf"]')
            input_el_google.fill(object_serch)
            page.keyboard.press("Enter")

        with allure.step(f'Кликнуть первую ссылку- результат поиска'):
            link_first = page.locator('div[class="v7W49e"] > div:first-child div[class="yuRUbf"] > a')
            link_first.click()

    @allure.title("Оформление заказа пиццы")
    def test_order_pizza(seif, web_driver_wait, page):
        """
                           Кейс №7

                           Шаги:
                          1. Открыть страницу http://pizzeria.skillbox.cc
                          2. Навести курсором мыши на Пиццу "4 в 1"
                          2.1. Нажать на кнопку "В корзину".
                          3. Навести курсор на середину картинки последней пиццы справа в слайдере.
                          3.1.В слайдере "Пиццы" нажать на стрелку "Вправо"
                          3.2. Нажать на пиццу. Пример: "Пепперони"
                          3.3. Нажать на кнопку "В корзину"
                          4. Нажать на иконку "Корзина" в правом верхнем углу сайта.
                          5. Нажать на кнопку "Перейти к оплате"
                          6. Нажать на раздел в хедере страницы "Мой аккаунт"
                          6.1.Нажать кнопку "Зарегистрироваться"
                          6.2. Заполнить поле "Имя пользователя": key
                          6.3. Заполнить поле "Адрес почты": key@bk.ru
                          6.4. Заполнить поле "Пароль": key
                          6.5. Нажать кнопку "Зарегистрироваться"
                          7. Нажать на иконку "Корзина" в правом верхнем углу сайта.
                          7.1. Нажать кнопку "Перейти к оплате"
                          8. Заполнить поля "Детали заказа":
                          ИМЯ: "Екатерина"
                          ФАМИЛИЯ: "Чудова"
                          Страна/Регион: "Россия"
                          Адрес: "Ленина 23-2"
                          Город/Населенный пункт: "Мурманск"
                          Область: "Мурманская область"
                          Почтовый индекс: "183032"
                          Телефон:"12345678911"
                          Адрес почты: "key@bk.ru" (Заполнен автоматически)
                          Дата заказа: Выбрать любую дату в будущем.
                          8.1. Выбрать способ оплаты: "Оплата при доставке"
                          8.2. Установить галочку в чек- боксе согласия с условиями вебсайта.
                          8.3. Нажать кнопку "Оформить заказ"
                          Проверить статус заказа:
                          9. Нажать на раздел " Мой аккаунт"
                          9.1. Нажать на раздел в меню "Мой аккаунт" "Заказы"
                          9.2. Нажать кнопку "Подробнее"
                           """

        nameuser = 'stepbystep'
        user_email = 'stepbystep@bk.ru'
        password_user = 'stepbystep23'
        url = 'http://pizzeria.skillbox.cc'
        logging.info(f"Запускаем страницу browser, URL {url}")
        with allure.step(f'Открыть страницу {url}'):
             page.goto(url, wait_until='domcontentloaded')

        with allure.step('Выбрать пиццу и нажать - В корзину'):
             object_first = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=425"]')
             object_first.hover()
             object_first.click()

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
             object_next = page.locator('a[class="slick-next"]')
             object_next.hover()
             object_next.click()

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
             object_second = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=417"]')
             object_second.hover()
             object_second.click()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
             object_basket = page.locator('a[class="cart-contents wcmenucart-contents"]')
             object_basket.click()

        with allure.step('Нажать на кнопку "Перейти к оплате"'):
             object_pay = page.locator('a[class="checkout-button button alt wc-forward"]')
             object_pay.click()

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
             my_account = page.locator('li[id="menu-item-30"] a')
             my_account.click()


        with allure.step('Нажать на кнопку войти'):
             page.locator('div.login-woocommerce').click()
             page.locator('#username').fill(nameuser)
             page.locator('#password').fill(password_user)
             page.locator('button[value="Войти"]').click()


        # with allure.step(f'Нажать кнопку "Зарегистрироваться"'):
        #      register_page = page.locator('button[class="custom-register-button"]')
        #      register_page.click()

        # with allure.step(f'Заполнить поле "Имя пользователя" {nameuser}'):
        #      input_username = page.locator('input[id="reg_username"]')
        #      input_username.fill(nameuser)

        # with allure.step(f'Заполнить поле "адрес почты" {user_email}'):
        #      input_email = page.locator('input[id="reg_email"]')
        #      input_email.fill(user_email)
        #
        # with allure.step(f'Заполнить поле "пароль" {password_user}'):
        #      input_password = page.locator('input[id="reg_password"]')
        #      input_password.fill(password_user)
        #
        # with allure.step(f'Нажать кнопку "Зарегистрироваться"'):
        #      registerbutton = page.locator('button[value="Зарегистрироваться"]')
        #      registerbutton.click()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
             object_basket = page.locator('a[class="cart-contents wcmenucart-contents"]')
             object_basket.click()

        with allure.step('Нажать на кнопку "Перейти к оплате"'):
            object_pay = page.locator('a[class="checkout-button button alt wc-forward"]')
            object_pay.click()

        with allure.step('Заполнить поля формы заказа.'):
            first_name = page.locator('#billing_first_name')
            first_name.fill('Екатерина')

            last_name = page.locator('#billing_last_name')
            last_name.fill('Чудова')

            billing_address = page.locator('#billing_address_1')
            billing_address.fill('Ленина 23-2')

            billing_city = page.locator('#billing_city')
            billing_city.fill('Мурманск')

            billing_state = page.locator('#billing_state')
            billing_state.fill('Мурманская область')

            billing_postcode = page.locator('#billing_postcode')
            billing_postcode.fill('183032')

            billing_phone = page.locator('#billing_phone')
            billing_phone.fill('890529785906')

            order_date_locator = page.locator('#order_date')
            order_date_locator.click()

            from datetime import datetime, timedelta

            def prefix_zero(n: int):
                """
                функция дописывает ноль перед чеслом n, если n<10
                :param n: целое число
                :return: строка
                """
                n_str = str(n)
                return "0" + n_str if n < 10 else n_str

            current_date = datetime.today() #текущая  дата
            delta = timedelta(days=5)
            order_date = current_date + delta

            day = prefix_zero(order_date.day)
            month = prefix_zero(order_date.month)
            year = str(order_date.year)

            page.keyboard.type(month)
            page.keyboard.type(day)
            page.keyboard.type(year)

        with allure.step('Выбрать способ оплаты radio-button: "Оплата при доставке"'):
            page.locator('#payment_method_cod').click()

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
            my_account = page.locator('li[id="menu-item-30"] a')
            my_account.click()

            orders = page.locator('li[class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--orders"] a')
            orders.click()

            orders = page.locator( 'div[class="woocommerce-MyAccount-content"] tbody tr:first-child td:last-child a')
            orders.click()

    @allure.title("Редактирование заказа")
    def test_order_edit(seif, web_driver_wait, page):
        """
                Кейс №8
                Предусловие: Пользователь должен быть Авторизован.
                Шаги:
               1. Открыть страницу http://pizzeria.skillbox.cc
               2. Навести курсором мыши на Пиццу "4 в 1"
               2.1. Нажать на кнопку "В корзину".
               3. Навести курсор на середину картинки последней пиццы справа в слайдере.
               3.1.В слайдере "Пиццы" нажать на стрелку "Вправо"
               3.2. Нажать на пиццу. Пример: "Пепперони"
               3.3. Нажать на кнопку "В корзину"
               4. Нажать на иконку "Корзина" в правом верхнем углу сайта.
               5. Нажать на кнопку "Перейти к оплате"
               6. Нажать на кнопку "Удалить" и удалить "Пиццу 4 в 1" из корзины.
               6. Выбрать подкатегорию в "Меню" -"Десерты".
               6.1.Нажать подкатегорию "Меню" -"Десерты"
               6.2. Нажать на иконку десерта "Шоколадный шок"
               6.3. Изменить количество десерта на "3"
               6.4. Нажать кнопку "В корзину"
               7. Нажать на иконку "Корзина" в правом верхнем углу сайта.
               7.1. Изменить количество пиццы "Пепперони"с 1 до 5
               7.1. Нажать кнопку "Обновить корзину"
        """

        nameuser = 'stepbystep'
        user_email = 'stepbystep@bk.ru'
        password_user = 'stepbystep23'
        url = 'http://pizzeria.skillbox.cc'
        logging.info(f"Запускаем страницу browser, URL {url}")
        with allure.step(f'Открыть страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
            my_account = page.locator('li[id="menu-item-30"] a')
            my_account.click()

        with allure.step('Нажать на кнопку войти'):
            page.locator('div.login-woocommerce').click()
            page.locator('#username').fill(nameuser)
            page.locator('#password').fill(password_user)
            page.locator('button[value="Войти"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Главная"'):
            main = page.locator('li[id="menu-item-26"] a')
            main.click()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            object_first = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=425"]')
            object_first.hover()
            object_first.click()

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            object_next = page.locator('a[class="slick-next"]')
            object_next.hover()
            object_next.click()

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            object_second = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=417"]')
            object_second.hover()
            object_second.click()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            object_basket = page.locator('a[class="cart-contents wcmenucart-contents"]')
            object_basket.click()

        with allure.step('Нажать на кнопку "Удалить" и удалить "Пиццу 4 в 1" из корзины.'):
            object_basket = page.locator('a[data-product_id="425"]')
            object_basket.click()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            object_menu = page.locator('li[id="menu-item-389"] > a')
            object_menu.hover()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            object_desert = page.locator('li[id="menu-item-391"] > a')
            object_desert.hover()
            object_desert.click()

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            desert_shoc = page.locator('li.post-435 a[class="collection_title"]')
            desert_shoc.click()

        with allure.step('Изменить количество десерта на "3"'):
            count0 = page.locator('input[name="quantity"]')
            count0.click()
            page.keyboard.press("Backspace")
            page.keyboard.type('3')

        with allure.step('Нажать кнопку "В корзину"'):
            page.locator('button[value="435"]').click()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            object_basket = page.locator('a[class="cart-contents wcmenucart-contents"]')
            object_basket.click()

        with allure.step('Изменить количество пиццы "Пепперони"с 1 до 5'):
            pizza_count = page.locator('//tr[.//a[contains(text(), "епперон")]]//input')
            pizza_count.click()
            page.keyboard.press("Backspace")
            page.keyboard.type('5')

        with allure.step('Нажать кнопку "Обновить корзину"'):
            inbasket = page.locator('td.actions > button')
            inbasket.click()

    @allure.title("Применение промокода при оформлении заказа.")
    def test_order_coupon(seif, web_driver_wait, page):
        """
           Кейс №9 - Сценарий №1
           Предусловие: Пользователь должен быть Авторизован.
           Шаги:
          1. Открыть страницу http://pizzeria.skillbox.cc
          2. Навести курсором мыши на Пиццу "4 в 1"
          2.1. Нажать на кнопку "В корзину".
          3. Навести курсор на середину картинки последней пиццы справа в слайдере.
          3.1.В слайдере "Пиццы" нажать на стрелку "Вправо"
          3.2. Нажать на пиццу. Пример: "Пепперони"
          3.3. Нажать на раздел в хедере страницы "Оформление заказа"
          4. Нажать на поле- ссылку для открытия поля- ввода купона.
          5. Ввести в поле- ввода купона GIVEMEHALYAVA.
          6. Нажать кнопку "Применить купон"
          7. Убедится, что сумма заказа уменьшилась на 10%
        """

        nameuser = 'stepbystep'
        password_user = 'stepbystep23'
        url = 'http://pizzeria.skillbox.cc'
        logging.info(f"Запускаем страницу browser, URL {url}")
        with allure.step(f'Открыть страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
            my_account = page.locator('li[id="menu-item-30"] a')
            my_account.click()

        with allure.step('Заполнить форму данными'):
            page.locator('div.login-woocommerce').click()
            page.locator('#username').fill(nameuser)
            page.locator('#password').fill(password_user)

        with allure.step('Нажать на кнопку войти'):
            page.locator('button[value="Войти"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Главная"'):
            page.locator('li[id="menu-item-26"] a').click()


        with allure.step('Выбрать пиццу "4 в 1" и нажать - В корзину'):
            object_first = page.locator('li[aria-hidden="false"] a[data-product_id="425"]')
            object_first.hover()
            object_first.click()

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            object_next = page.locator('a[class="slick-next"]')
            object_next.click()

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            object_second = page.locator('li[aria-hidden="false"] a[data-product_id="417"]')
            object_second.hover()
            object_second.click()

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            my_order = page.locator('li[id="menu-item-31"] a')
            my_order.click()

        with allure.step('Нажать на поле- ссылку для открытия поля- ввода купона"'):
            showcoupon = web_driver_wait('a[class ="showcoupon"]')
            showcoupon.click()

        # todo Ссылка нажимается раньше, чем ей назначен обработчик click.
        #  Реализовать цыкл в котором будет происходить клик на ссылке до тех пор пока не отработает обработчик.

        with allure.step('Ввести в поле- ввода купона GIVEMEHALYAVA'):
            coupon_code = web_driver_wait('input[id="coupon_code"]')
            coupon_code.fill('GIVEMEHALYAVA')

        with allure.step('Нажать кнопку "применить купон'):
            apply_coupon = page.locator('button[name = "apply_coupon"]')
            apply_coupon.click()


        with allure.step('Убедится, что сумма заказа уменьшилась на 10%'):
            percent = 10
            discount = percent/100
            total_summ_order = page.locator('tr.cart-subtotal>td>span').inner_text()[0:-1].replace(',','.')
            total_summ_order = float(total_summ_order)

            discount_order = page.locator('tr.cart-discount>td>span').inner_text()[0:-1].replace(',','.')
            discount_order = float(discount_order)

            discount_summ = page.locator('tr.order-total>td span.amount').inner_text()[0:-1].replace(',','.')
            discount_summ = float(discount_summ)

            assert total_summ_order*discount == total_summ_order-discount_summ, f"Сумма скидки не равна {percent}%"


    @allure.title("Применение невалидного промокода при оформлении заказа.")
    def test_order_wrongcoupon(seif, web_driver_wait, page):
            """
                               Кейс №10 - Сценарий №2
                               Предусловие: Пользователь должен быть Авторизован.
                               Шаги:
                              1. Открыть страницу http://pizzeria.skillbox.cc
                              2. Навести курсором мыши на Пиццу "4 в 1"
                              2.1. Нажать на кнопку "В корзину".
                              3. Навести курсор на середину картинки последней пиццы справа в слайдере.
                              3.1.В слайдере "Пиццы" нажать на стрелку "Вправо"
                              3.2. Нажать на пиццу. Пример: "Пепперони"
                              3.3. Нажать на раздел в хедере страницы "Оформление заказа"
                              4. Нажать на поле- ссылку для открытия поля- ввода купона.
                              5. Ввести в поле- ввода купона "DC120".
                              6. Нажать кнопку "применить купон".

                               """

            nameuser = 'stepbystep'
            password_user = 'stepbystep23'
            url = 'http://pizzeria.skillbox.cc'
            logging.info(f"Запускаем страницу browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                my_account = page.locator('li[id="menu-item-30"] a')
                my_account.click()

            with allure.step('Нажать на кнопку войти'):
                page.locator('div.login-woocommerce').click()
                page.locator('#username').fill(nameuser)
                page.locator('#password').fill(password_user)
                page.locator('button[value="Войти"]').click()

            with allure.step('Нажать на раздел в хедере страницы "Главная"'):
                main = page.locator('li[id="menu-item-26"] a')
                main.click()

            with allure.step('Выбрать пиццу и нажать - В корзину'):
                object_first = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=425"]')
                object_first.hover()
                object_first.click()

            with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
                object_next = page.locator('a[class="slick-next"]')
                object_next.hover()
                object_next.click()

            with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
                object_second = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=417"]')
                object_second.hover()
                object_second.click()

            with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
                my_order = page.locator('li[id="menu-item-31"] a')
                my_order.click()

            with allure.step('Нажать на поле- ссылку для открытия поля- ввода купона"'):
                showcoupon = page.locator(' a[class ="showcoupon"]')
                showcoupon.click()

            with allure.step('Ввести в поле- ввода купона невалидный купон'):
                coupon_code = page.locator('input[id = "coupon_code"]')
                coupon_code.fill('DC120')

            with allure.step('Нажать кнопку "применить купон'):
                apply_coupon = page.locator('button[name = "apply_coupon"]')
                apply_coupon.click()


            with allure.step('Проверяем, что купон не применился'):

                total_summ_order = page.locator('tr.cart-subtotal>td>span').inner_text()[0:-1].replace(',', '.')
                total_summ_order = float(total_summ_order)

                # discount_order = page.locator('tr.cart-discount>td>span').inner_text()[0:-1].replace(',', '.')
                # discount_order = float(discount_order)

                discount_summ = page.locator('tr.order-total>td span.amount').inner_text()[0:-1].replace(',', '.')
                discount_summ = float(discount_summ)

                assert discount_summ == total_summ_order, "Пользователь получил скидку в результате применения невалидного купона"

    @allure.title("Перехватить промокод GIVEMEHALYAVA.")
    def test_order_block_coupon(seif, web_driver_wait, page):
            """
                    Кейс №11 - Сценарий №3
                    Предусловие: Пользователь должен быть Авторизован.
                    Шаги:
                    1. Открыть страницу http://pizzeria.skillbox.cc
                    2. Навести курсором мыши на Пиццу "Рай"
                    2.1. Нажать на кнопку "В корзину".
                    3. Нажать на раздел в хедере страницы "Оформление заказа"
                    4. Нажать на поле- ссылку для открытия поля- ввода купона.
                    5. Ввести в поле- ввода купона GIVEMEHALYAVA.
                    6. Нажать кнопку "Применить купон"
                    7.ПЕРЕХВАТИТЬ КУПОН!!!!
            """

            nameuser = 'stepbystep'
            password_user = 'stepbystep23'
            url = 'http://pizzeria.skillbox.cc'
            logging.info(f"Запускаем страницу browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                my_account = page.locator('li[id="menu-item-30"] a')
                my_account.click()

            with allure.step('Нажать на ссылку войти в хедере'):
                page.locator('div.login-woocommerce').click()

            with allure.step('Заполнить поля учетными данными пользователя'):
                page.locator('#username').fill(nameuser)
                page.locator('#password').fill(password_user)

            with allure.step('Нажать на кнопку войти'):
                page.locator('button[value="Войти"]').click()

            with allure.step('Нажать на раздел в хедере страницы "Главная"'):
                main = page.locator('li[id="menu-item-26"] a')
                main.click()

            with allure.step('Выбрать пиццу и нажать - В корзину'):
                object_first = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=425"]')
                object_first.hover()
                object_first.click()

            with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
                 object_next = page.locator('a[class="slick-next"]')
                 object_next.hover()
                 object_next.click()

            with allure.step('Выбрать пиццу Рай и Нажать на кнопку -В корзину'):
                 object_second = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=421"]')
                 object_second.hover()
                 object_second.click()

            with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
                  my_order = page.locator('li[id="menu-item-31"] a')
                  my_order.click()

            with allure.step('Нажать на поле- ссылку для открытия поля- ввода купона"'):
                  showcoupon = page.locator(' a[class ="showcoupon"]')
                  showcoupon.click()

            with allure.step('Ввести в поле- ввода купона GIVEMEHALYAVA'):
                  coupon_code = page.locator('input[id = "coupon_code"]')
                  coupon_code.fill('GIVEMEHALYAVA')

            with allure.step('Нажать кнопку "применить купон'):
                  apply_coupon = page.locator('button[name = "apply_coupon"]]')
                  apply_coupon.click()

    @allure.title("Применение промокода ПОВТОРНО при оформлении заказа.")
    def test_order_pizza(seif, web_driver_wait, page, goto_to, authorization):
        #todo  Кейс №12 - Сценарий №4
        """
                            Кейс №12 - Сценарий №4
                          Предусловие: Пользователь должен быть Авторизован.
                    Шаги:
                    1. Открыть страницу http://pizzeria.skillbox.cc
                    2. Навести курсором мыши на Пиццу "Рай"
                    2.1. Нажать на кнопку "В корзину".
                    3. Нажать на раздел в хедере страницы "Оформление заказа"
                    4. Нажать на поле- ссылку для открытия поля- ввода купона.
                    5. Ввести в поле- ввода купона GIVEMEHALYAVA.
                    6. Нажать кнопку "Применить купон"
                    7. До заполнить на странице "Оформление заказа" обязательные поля не заполненные по умолчанию: дата заказа.
                    8.Установить галочку в чек- боксе согласия с условиями вебсайта.
                    9. Нажать кнопку "Оформить заказ"
                    10.Выбрать подкатегорию в "Меню" -"Десерты".
                    10.1.Нажать подкатегорию "Меню" -"Десерты"
                    10.2. Нажать на иконку десерта "Шоколадный шок"
                    10.3. Нажать на кнопку "В корзину".
                    11. Нажать на раздел в хедере страницы "Оформление заказа"
                    12. Нажать на поле- ссылку для открытия поля- ввода купона.
                    13. Ввести в поле- ввода купона GIVEMEHALYAVA.
                    14. Нажать кнопку "Применить купон"
                    15. До заполнить на странице "Оформление заказа" обязательные поля не заполненные по умолчанию: дата заказа.
                    16.Установить галочку в чек- боксе согласия с условиями вебсайта.
                    17. Нажать кнопку "Оформить заказ"
        """
        goto_to()
        authorization()


        with allure.step('Нажать на раздел в хедере страницы "Главная"'):
            main = page.locator('li[id="menu-item-26"] a')
            main.click()

        with allure.step('Выбрать пиццу "Рай" и нажать - В корзину'):
            object_first = page.locator('li[aria-hidden="false"] a[href="?add-to-cart=421"]')
            object_first.hover()
            object_first.click()

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            my_order = page.locator('li[id="menu-item-31"] a')
            my_order.click()

        with allure.step('Нажать на поле- ссылку для открытия поля- ввода купона"'):
            showcoupon = page.locator(' a[class ="showcoupon"]')
            showcoupon.click()

        with allure.step('Ввести в поле- ввода купона GIVEMEHALYAVA'):
            coupon_code = page.locator('input[id = "coupon_code"]')
            coupon_code.fill('GIVEMEHALYAVA')

        with allure.step('Нажать кнопку "применить купон'):
            apply_coupon = page.locator('button[name = "apply_coupon"]')
            apply_coupon.click()

    def prefix_zero(n: int):
        """
                функция дописывает ноль перед чеслом n, если n<10
                :param n: целое число
                :return: строка
        """
        n_str = str(n)
        return "0" + n_str if n < 10 else n_str

        current_date = datetime.today()  # текущая  дата
        delta = timedelta(days=5)
        order_date = current_date + delta

        day = prefix_zero(order_date.day)
        month = prefix_zero(order_date.month)
        year = str(order_date.year)

        page.keyboard.type(month)
        page.keyboard.type(day)
        page.keyboard.type(year)

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
             page.locator('#place_order').click()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            object_desert = page.locator('li[id="menu-item-391"] > a')
            object_desert.hover()
            object_desert.click()

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            page.locator('li.post-435 a[class="collection_title"]').hover()
            page.locator('li.post-435 a[class="collection_title"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
                my_order = page.locator('li[id="menu-item-31"] a')
                my_order.click()

        with allure.step('Нажать на поле- ссылку для открытия поля- ввода купона"'):
                showcoupon = page.locator(' a[class ="showcoupon"]')
                showcoupon.click()

        with allure.step('Ввести в поле- ввода купона GIVEMEHALYAVA'):
                coupon_code = page.locator('input[id = "coupon_code"]')
                coupon_code.fill('GIVEMEHALYAVA')

        with allure.step('Нажать кнопку "применить купон'):
                apply_coupon = page.locator('button[name = "apply_coupon"]]')
                apply_coupon.click()

        def prefix_zero(n: int):
            """
                    функция дописывает ноль перед чеслом n, если n<10
                    :param n: целое число
                    :return: строка
            """
            n_str = str(n)
            return "0" + n_str if n < 10 else n_str

            current_date = datetime.today()  # текущая  дата
            delta = timedelta(days=5)
            order_date = current_date + delta

            day = prefix_zero(order_date.day)
            month = prefix_zero(order_date.month)
            year = str(order_date.year)

            page.keyboard.type(month)
            page.keyboard.type(day)
            page.keyboard.type(year)

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
                page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
                page.locator('#place_order').click()

    @allure.title("Зарегистрироваться в бонусной программе")
    def test_red_bonus(seif, web_driver_wait, page):
        """
                            Кейс №13 - Сценарий №5
                    Предусловие: Пользователь должен быть Авторизован.
                    Шаги:
                    1. Открыть страницу http://pizzeria.skillbox.cc
                    2. Нажать на раздел в хедере страницы "Бонусная программа"
                    2.1. Ввести данные в поле имя.
                    2.2. Ввести данные в поле телефон.
                    3. Нажать кнопку "Оформить карту"

        """

        nameuser = 'stepbystep'
        password_user = 'stepbystep23'
        url = 'http://pizzeria.skillbox.cc'
        logging.info(f"Запускаем страницу browser, URL {url}")

        with allure.step(f'Открыть страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
            my_account = page.locator('li[id="menu-item-30"] a')
            my_account.click()

        with allure.step('Нажать на кнопку войти'):
            page.locator('div.login-woocommerce').click()
            page.locator('#username').fill(nameuser)
            page.locator('#password').fill(password_user)
            page.locator('button[value="Войти"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Бонусная программа"'):
            page.locator('li[id="menu-item-363"] a').click()

        with allure.step('Заполнить поля имя и телефон'):
            page.locator('input[name="username"]').fill('Екатерина')
            page.locator('input[id="bonus_phone"]').fill('89095608899')

        with allure.step('Нажать кнопку "Оформить карту"'):
            page.locator('button[name="bonus"]').click()

    @allure.title("Проверить применение скидки 15% по № телефона (бонусная программа)")
    def test_check_bonus(seif, web_driver_wait, page):
        """
                                    Кейс №14- Сценарий №6
                    Предусловие: Пользователь должен быть Авторизован и зарегистрирован в бонусной программе.
                    Шаги:
                    1. Открыть страницу http://pizzeria.skillbox.cc
                    2.Выбрать подкатегорию в "Меню" -"Десерты".
                    3.Нажать подкатегорию "Меню" -"Десерты"
                    4. Нажать на иконку десерта "Шоколадный шок"
                    5. Нажать на кнопку "В корзину".
                    6. Нажать на раздел в хедере страницы "Оформление заказа"
                    7. Нажать на поле- ссылку для открытия поля- ввода купона.
                    8. Ввести в поле- комментария номер телефона '89095608899'.
                    9. До заполнить на странице "Оформление заказа" обязательные поля не заполненные по умолчанию: дата заказа.
                    10.Установить галочку в чек- боксе согласия с условиями вебсайта.
                    11. Нажать кнопку "Оформить заказ"
                    12. Убедиться, что применилась скидка 15%

        """

        nameuser = 'stepbystep'
        password_user = 'stepbystep23'
        url = 'http://pizzeria.skillbox.cc'
        logging.info(f"Запускаем страницу browser, URL {url}")

        with allure.step(f'Открыть страницу {url}'):
            page.goto(url, wait_until='domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
            my_account = page.locator('li[id="menu-item-30"] a')
            my_account.click()

        with allure.step('Нажать на кнопку войти'):
            page.locator('div.login-woocommerce').click()
            page.locator('#username').fill(nameuser)
            page.locator('#password').fill(password_user)
            page.locator('button[value="Войти"]').click()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            object_desert = page.locator('li[id="menu-item-391"] > a')
            object_desert.hover()
            object_desert.click()

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            page.locator('li.post-435 a[class="collection_title"]').hover()
            page.locator('li.post-435 a[class="collection_title"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
                my_order = page.locator('li[id="menu-item-31"] a')
                my_order.click()

        with allure.step('Ввести в поле- комментария номер телефона 89095608899'):
             page.locator('#order_comments').fill('89095608899')

        def prefix_zero(n: int):
            """
                    функция дописывает ноль перед чеслом n, если n<10
                    :param n: целое число
                    :return: строка
            """
            n_str = str(n)
            return "0" + n_str if n < 10 else n_str

            current_date = datetime.today()  # текущая  дата
            delta = timedelta(days=5)
            order_date = current_date + delta

            day = prefix_zero(order_date.day)
            month = prefix_zero(order_date.month)
            year = str(order_date.year)

            page.keyboard.type(month)
            page.keyboard.type(day)
            page.keyboard.type(year)

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
                page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
                page.locator('#place_order').click()

        @allure.title('Проверить валидацию полей раздела "Бонусная программа"')
        def test_checkstring_bonus(seif, web_driver_wait, page):
            """
                                        Кейс №15- Сценарий №6
                                Предусловие: Пользователь должен быть Авторизован и зарегистрирован в бонусной программе.
                                Шаги:
                                1. Открыть страницу http://pizzeria.skillbox.cc
                                2. Нажать на раздел в хедере страницы "Бонусная программа"
                                2.1. Ввести данные в поле имя.
                                2.2. Ввести данные в поле телефон.
                                3. Нажать кнопку "Оформить карту"

            """

            nameuser = 'stepbystep'
            password_user = 'stepbystep23'
            url = 'http://pizzeria.skillbox.cc'
            logging.info(f"Запускаем страницу browser, URL {url}")

            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                my_account = page.locator('li[id="menu-item-30"] a')
                my_account.click()

            with allure.step('Нажать на кнопку войти'):
                page.locator('div.login-woocommerce').click()
                page.locator('#username').fill(nameuser)
                page.locator('#password').fill(password_user)
                page.locator('button[value="Войти"]').click()

            with allure.step('Нажать на раздел в хедере страницы "Бонусная программа"'):
                page.locator('li[id="menu-item-363"] a').click()

            with allure.step('Заполнить поля имя и телефон'):
                page.locator('input[name="username"]').fill('Екатерина')
                page.locator('input[id="bonus_phone"]').fill('89095608899')

            with allure.step('Нажать кнопку "Оформить карту"'):
                page.locator('button[name="bonus"]').click()

        phone = generation_random_digits(10)
        string_user = ['', ' Катя ', '`~@#$%^&*()_+|-=\{}[]:', 'ТАНЯ', '<script>alert(‘XSS’)</script>', phone,
                       generation_random_string(255)]

        string_phon = [generation_random_digits(10), generation_random_digits(11), generation_random_digits(12), ' '+generation_random_digits(11)+' ', '',
                       '<script>alert(‘XSS’)</script>', generation_random_digits(255), '1', "tr'"]

        pass