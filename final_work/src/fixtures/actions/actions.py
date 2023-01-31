import logging
import allure
import pytest
from time import sleep
from final_work.src.Utils.сhecking_elements import *  # noqa
from datetime import datetime, timedelta


class Actions:

    @pytest.fixture
    def goto_to(self, page):
        def callback(url='http://pizzeria.skillbox.cc'):
            logging.info(f"Запускаем страницу browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

        return callback

    @pytest.fixture()
    def user_registration(self, page, pytestconfig):
        def callback(nameuser=pytestconfig.getini('nameuser'),
                     user_email=pytestconfig.getini('user_email'),
                     password_user=pytestconfig.getini('password_user')):
            with allure.step(f'Нажать кнопку "Зарегистрироваться"'):
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

        return callback

    @pytest.fixture()
    def price_parser(self, page):
        def callback(locator: str):
            price_parser_el = page.locator(locator).inner_text()[0:-1].replace(',', '.')
            price_parser_el = float(price_parser_el)
            return price_parser_el

        return callback

    @pytest.fixture()
    def fill_order_form(self, page):
        def callback():
            with allure.step('Заполнить поля формы заказа.'):
                page.locator('#billing_first_name').fill('Екатерина')
                page.locator('#billing_last_name').fill('Чудова')
                page.locator('#billing_address_1').fill('Ленина 23-2')
                page.locator('#billing_city').fill('Мурманск')
                page.locator('#billing_state').fill('Мурманская область')
                page.locator('#billing_postcode').fill('183032')
                page.locator('#billing_phone').fill('890529785906')

        return callback
