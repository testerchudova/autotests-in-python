import logging
import allure
import pytest
from time import sleep
from final_work.src.Utils.сhecking_elements import *  # noqa
from datetime import datetime, timedelta
from pathlib import Path


class Actions:

    @pytest.fixture
    def goto_to(self, page):
        def callback(url='http://pizzeria.skillbox.cc'):
            logging.info(f"Загрузка страницы browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

        return callback

    @pytest.fixture()
    def user_registration(self, page, pytestconfig):
        def callback(nameuser=pytestconfig.getini('nameuser'),
                     user_email=pytestconfig.getini('user_email'),
                     password_user=pytestconfig.getini('password_user')):
            logging.info('\nЗаполнение формы "Регистрация пользователя"\n'
                         f'nameuser = {nameuser}\n'
                         f'user_email = {user_email}\n'
                         f'password_user = {password_user}\n')

            with allure.step('Нажать кнопку "Зарегистрироваться"'):
                page.locator('button[class="custom-register-button"]').click()

            with allure.step(f'Заполнить поле "Имя пользователя" {nameuser}'):
                page.locator('input[id="reg_username"]').fill(nameuser)

            with allure.step(f'Заполнить поле "адрес почты" {user_email}'):
                page.locator('input[id="reg_email"]').fill(user_email)

            with allure.step(f'Заполнить поле "пароль" {password_user}'):
                page.locator('input[id="reg_password"]').fill(password_user)

            with allure.step('Нажать кнопку "Зарегистрироваться"'):
                page.locator('button[value="Зарегистрироваться"]').click()

            with allure.step('Проверка, зарегистрировался ли пользователь'):
                assert nameuser.upper() in page.locator(
                    '.user-name').inner_text().upper(), 'Пользователь не прошел регистрацию'

        return callback

    @pytest.fixture
    def authorization(self, page, pytestconfig):
        def callback(nameuser=pytestconfig.getini('nameuser'), password_user=pytestconfig.getini('password_user')):
            logging.info(f'\nЗаполнение формы "авторизация пользователя" \n'
                         f'nameuser = {nameuser}\n'
                         f'password_user = {password_user}')

            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                page.locator('li[id="menu-item-30"] a').click()

            with allure.step('Нажать на ссылку войти в хедере'):
                page.locator('div.login-woocommerce').click()

            with allure.step('Заполнить поля учетными данными пользователя'):
                page.locator('#username').fill(nameuser)
                page.locator('#password').fill(password_user)

            with allure.step('Нажать на кнопку войти'):
                page.locator('button[value="Войти"]').click()

        return callback

    @pytest.fixture()
    def click_on_main(self, page):
        def callback():
            with allure.step('Нажать на раздел в хедере страницы "Главная"'):
                page.locator('li[id="menu-item-26"] a').click()
            page.wait_for_event('domcontentloaded')

        return callback

    @pytest.fixture()
    def click_my_account(self, page):
        def callback():
            with allure.step('Нажать на раздел в хедере страницы "Мой аккаунт"'):
                page.locator('li[id="menu-item-30"] a').click()

        return callback

    @pytest.fixture()
    def coupon_entry(self, page):
        def callback(name_coupon='GIVEMEHALYAVA', second=0.5):
            logging.info(f'Применение купона {name_coupon}')
            count_time = 0
            while count_time < 10:
                count_time += 1

                if 'none' in page.locator('.checkout_coupon').get_attribute('style'):
                    with allure.step('Нажать на поле - ссылку для открытия поля - ввода купона"'):
                        page.locator('a[class ="showcoupon"]').click()
                else:
                    with allure.step(f'Ввести в поле- ввода купона {name_coupon}'):
                        page.locator('input[id = "coupon_code"]').fill(name_coupon)

                    with allure.step('Нажать кнопку "применить купон'):
                        page.locator('button[name = "apply_coupon"]').click()

                    break

                sleep(second)
                logging.info(f'Ожидание {second * count_time}сек')

        return callback

    @pytest.fixture()
    def checking_discount(self, page, price_parser, web_driver_wait):
        def callback(percent_discount=10):
            logging.info('Проверяем, применилась ли скидка')
            discount = percent_discount / 100
            web_driver_wait('tr.cart-subtotal>td>span')
            total_summ_order = price_parser('tr.cart-subtotal>td>span')
            discount_summ = price_parser('tr.order-total>td span.amount')
            logging.info(f'\nСкидка: {percent_discount}%\n'
                         f'Полная сумма: {total_summ_order}р\n'
                         f'Сумма после применения скидки: {discount_summ}р\n')

            return total_summ_order * discount == total_summ_order - discount_summ

        return callback

    @pytest.fixture()
    def point_and_click(self, page):
        def callback(locator: str):
            object = page.locator(locator)
            object.hover()
            object.click()

        return callback

    @pytest.fixture()
    def order_date(self, page):
        def callback(count_days=5):
            with allure.step('Заполнить дату заказа'):
                page.locator('#order_date').click()

                current_date = datetime.today()  # текущая  дата
                delta = timedelta(count_days)
                order_date = current_date + delta

                day = prefix_zero(order_date.day)
                month = prefix_zero(order_date.month)
                year = str(order_date.year)

                page.keyboard.type(month)
                page.keyboard.type(day)
                page.keyboard.type(year)

                logging.info(f'Запонение поля "Дата доставки" датой {day}.{month}.{year}')

        return callback

    @pytest.fixture()
    def price_parser(self, page):
        def callback(locator: str):
            price_parser_el = page.locator(locator).inner_text()[0:-1].replace(',', '.')
            price_parser_el = float(price_parser_el)
            return price_parser_el

        return callback

    @pytest.fixture()
    def fill_order_form(self, page, pytestconfig):
        fields_content = {'first_name': 'Екатерина',
                          'last_name': 'Чудова',
                          'address': 'Ленина 23 - 2',
                          'city': 'Мурманск',
                          'state': 'Мурманская область',
                          'postcode': pytestconfig.getini('postcode'),
                          'phone': pytestconfig.getini('telephone'),
                          'email': pytestconfig.getini('user_email')
                          }

        def callback(field_content=None):
            field_content = fields_content if field_content is None else field_content

            form_fields = {"first_name": page.locator('#billing_first_name'),
                           'last_name': page.locator('#billing_last_name'),
                           'address': page.locator('#billing_address_1'),
                           'city': page.locator('#billing_city'),
                           'state': page.locator('#billing_state'),
                           'postcode': page.locator('#billing_postcode'),
                           'phone': page.locator('#billing_phone'),
                           'email': page.locator('input#billing_email')
                           }
            with allure.step('Заполнить поля формы заказа.'):
                logging.info('Запонение полей формы "Детали заказа"')
                for key in form_fields:
                    logging.info(f'{key} = {field_content[key]}')
                    form_fields[key].fill(field_content[key])

        return callback

    @pytest.fixture()
    def screenshot_el(self, page):
        current_path = Path(__file__)

        def callback(name_files, selector='div.woocommerce', path='screenshots'):
            screenshots_path = current_path.parents[3].joinpath(path, name_files)
            page.locator(selector).screenshot(
                path=screenshots_path)

            logging.info(f'Сохранение screenshot в {screenshots_path}')

        return callback

    @pytest.fixture()
    def clear_trash(self, page, web_driver_wait):
        def callback():

            logging.info('Перейти в раздел карзина, нажата кнопка "Корзина"')
            web_driver_wait('li#menu-item-29').click()

            logging.info('Ожидание загрузки раздела "Корзина"')
            page.wait_for_event('domcontentloaded')

            if is_element(page, 'tr.cart-discount'):
                logging.info('Удаление купона')
                web_driver_wait('a.woocommerce-remove-coupon').click()

            td = page.locator('td a.remove')
            td_count = td.count()
            for i in range(td_count):
                first = web_driver_wait('tr.woocommerce-cart-form__cart-item.cart_item').first
                remove_el = first.locator('td a.remove')
                name_product = first.locator('td.product-name a').inner_text()
                remove_el.click()
                logging.info(f'Удаление продукта {name_product}')

        return callback
