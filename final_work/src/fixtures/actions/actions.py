import logging
import allure
import pytest


class Actions:

    @pytest.fixture
    def goto_to(self, page):
        def callback(url='http://pizzeria.skillbox.cc'):
            logging.info(f"Запускаем страницу browser, URL {url}")
            with allure.step(f'Открыть страницу {url}'):
                page.goto(url, wait_until='domcontentloaded')

        return callback

    @pytest.fixture
    def authorization(self, page, pytestconfig):
        def callback(nameuser = pytestconfig.getini('nameuser'), password_user = pytestconfig.getini('password_user')):
            # nameuser = pytestconfig.getini('nameuser')
            # password_user = pytestconfig.getini('password_user')

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
        def callback(self, name_coupon='GIVEMEHALYAVA'):
            with allure.step(f'Ввести в поле- ввода купона {name_coupon}'):
                coupon_code = page.locator('input[id = "coupon_code"]')
                coupon_code.fill(name_coupon)

            with allure.step('Нажать кнопку "применить купон'):
                apply_coupon = page.locator('button[name = "apply_coupon"]').click()
                apply_coupon

        return callback
