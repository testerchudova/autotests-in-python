import logging
from time import sleep
from datetime import datetime, timedelta
import allure
from pathlib import Path
from random import uniform
import pytest
from final_work.src.Utils.сhecking_elements import *  # noqa
from final_work.src.actions.actions import *  # noqa
from final_work.src.fixtures import Actions

current_path = Path(__file__)


class TestExample(Actions):

    @allure.title("Регистрация пользователя")
    def test_user_registration(seif,
                               page,
                               goto_to,
                               pytestconfig,
                               click_my_account,
                               user_registration):
        """
        Кейс №1
        1. Открыть страницу http://pizzeria.skillbox.cc
        2. Нажать на раздел в хедере страницы "Мой аккаунт"
            2.1.Нажать кнопку "Зарегистрироваться"
            2.2. Заполнить поле "Имя пользователя": key
            2.3. Заполнить поле "Адрес почты": key@bk.ru
            2.4. Заполнить поле "Пароль": key
            2.5. Нажать кнопку "Зарегистрироваться"
        """

        goto_to()
        click_my_account()
        user_registration()

    @allure.title("Оформление заказа пиццы")
    def test_order_pizza(seif,
                         page,
                         goto_to,
                         authorization,
                         click_my_account,
                         point_and_click,
                         order_date,
                         fill_order_form):
        """
               Кейс №2
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
              6.1.Нажать на ссылку "Войти"
              6.2. Заполнить поле "Имя пользователя":
              6.4. Заполнить поле "Пароль":
              6.5. Нажать кнопку "Войти"
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

        goto_to()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=417"]')

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            page.locator('a[class="cart-contents wcmenucart-contents"]').click()

        with allure.step('Нажать на кнопку "Перейти к оплате"'):
            page.locator('a[class="checkout-button button alt wc-forward"]').click()

        click_my_account()
        authorization()
        fill_order_form()
        order_date()

        with allure.step('Выбрать способ оплаты radio-button: "Оплата при доставке"'):
            page.locator('#payment_method_cod').click()

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

            click_my_account()

        with allure.step('Нажать кнопку "Заказы"'):
            orders = page.locator(
                'li[class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--orders"] a')
            orders.click()

        with allure.step('Нажать кнопку подробнее'):
            orders = page.locator('div[class="woocommerce-MyAccount-content"] tbody tr:first-child td:last-child a')
            orders.click()

        with allure.step('Проверка результата нажатия кнопки'):
            assert is_element(page, '.order-date'), "При нажатии кнопки действие не произошло"

    @allure.title("Редактирование заказа")
    def test_order_edit(seif,
                        page,
                        goto_to,
                        authorization,
                        click_on_main,
                        click_my_account,
                        point_and_click):
        """
                Кейс №3
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

        goto_to()
        click_my_account()
        authorization()
        click_on_main()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=417"]')

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            page.locator('a[class="cart-contents wcmenucart-contents"]').click()

        with allure.step('Нажать на кнопку "Удалить" и удалить "Пиццу 4 в 1" из корзины.'):
            page.locator('a[data-product_id="425"]').click()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            page.locator('li[id="menu-item-389"] > a').hover()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            point_and_click('li[id="menu-item-391"] > a')

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            page.locator('li.post-435 a[class="collection_title"]').click()

        with allure.step('Изменить количество десерта на "3"'):
            page.locator('input[name="quantity"]').click()
            page.keyboard.press("Backspace")
            page.keyboard.type('3')

        with allure.step('Нажать кнопку "В корзину"'):
            page.locator('button[value="435"]').click()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            page.locator('a[class="cart-contents wcmenucart-contents"]').click()

        with allure.step('Изменить количество пиццы "Пепперони"с 1 до 5'):
            page.locator('//tr[.//a[contains(text(), "епперон")]]//input').click()
            page.keyboard.press("Backspace")
            page.keyboard.type('5')

        with allure.step('Нажать кнопку "Обновить корзину"'):
            page.locator('td.actions > button').click()

    @allure.title("Применение промокода при оформлении заказа.")
    def test_order_coupon(seif,
                          page,
                          goto_to,
                          authorization,
                          click_on_main,
                          click_my_account,
                          point_and_click,
                          coupon_entry,
                          price_parser):
        """
           Кейс №5 - Сценарий №1
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

        goto_to()
        click_my_account()
        authorization()
        click_on_main()

        with allure.step('Выбрать пиццу "4 в 1" и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[data-product_id="425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            page.locator('a[class="slick-next"]').click()

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[data-product_id="417"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()

        with allure.step('Убедится, что сумма заказа уменьшилась на 10%'):
            percent = 10
            discount = percent / 100
            total_summ_order = price_parser('tr.cart-subtotal>td>span')
            discount_summ = price_parser('tr.order-total>td span.amount')

        if total_summ_order * discount != total_summ_order - discount_summ:
            page.locator('div.woocommerce').screenshot(
                path=r"D:\Ekaterina\autotests-in-python\final_work\tests\screen_GIVEMEHALYAVA.png")
            raise Exception(f"Сумма скидки не равна {percent}%")

        # assert total_summ_order * discount == total_summ_order - discount_summ, f"Сумма скидки не равна {percent}%"
        # pass

    @allure.title("Применение невалидного промокода при оформлении заказа.")
    def test_order_wrongcoupon(seif,
                               page,
                               goto_to,
                               authorization,
                               click_on_main,
                               click_my_account,
                               point_and_click,
                               coupon_entry,
                               price_parser):

        """
              Кейс №6 - Сценарий №2
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

        goto_to()
        click_my_account()
        authorization()
        click_on_main()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=417"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()

        with allure.step('Проверяем, что купон не применился'):
            total_summ_order = price_parser('tr.cart-subtotal>td>span')
            discount_summ = price_parser('tr.order-total>td span.amount')

            # if discount_summ != total_summ_order:
            #     screenshots = str(current_path.parent.parent) + "\\screenshot\\"
            #     page.locator('div.woocommerce').screenshot(
            #         path=screenshots + "screenshot.png")
            #     raise Exception("Пользователь получил скидку в результате применения невалидного купона")
            assert discount_summ == total_summ_order, 'Пользователь получил скидку в результате применения невалидного купона'

    @allure.title("Перехватить промокод GIVEMEHALYAVA.")
    def test_order_block_coupon(seif,
                                page,
                                goto_to,
                                authorization,
                                click_on_main,
                                click_my_account,
                                point_and_click,
                                coupon_entry):
        # todo  Кейс №7. ПЕРЕХВАТИТЬ КУПОН!!!!
        """
                Кейс №7 - Сценарий №3
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

        goto_to()
        click_my_account()
        authorization()
        click_on_main()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Рай и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=421"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()

    @allure.title("Применение промокода ПОВТОРНО при оформлении заказа.")
    def test_reapplying_promo_code(seif,
                                   page,
                                   goto_to,
                                   user_registration,
                                   coupon_entry,
                                   click_on_main,
                                   point_and_click,
                                   order_date,
                                   fill_order_form,
                                   click_my_account,
                                   price_parser,
                                   authorization,
                                   web_driver_wait):
        # todo  Кейс №8
        """
            Кейс №8 - Сценарий №4
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
        nameuser = f'Ekaterina{generation_random_digits(5)}'
        user_email = f'{nameuser}@bk.ru'
        password_user = generation_random_string(12)

        goto_to()
        click_my_account()
        # user_registration(nameuser=nameuser, user_email=user_email, password_user=password_user)
        authorization()
        click_on_main()

        with allure.step('Выбрать пиццу "Рай" и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=421"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()
        order_date()
        fill_order_form()

        with allure.step('Установить галочку в чек - боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()



        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

            page.wait_for_event('domcontentloaded')

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            page.locator('li[id="menu-item-389"] > a').hover()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            point_and_click('li[id="menu-item-391"] > a')

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            point_and_click('li.post-435 a[class="collection_title"]')

        page.wait_for_event('domcontentloaded')
        #
        #
        # def wait_event(fn_action, fn_predicate, fn_event_execution=None, second=0.5):
        #     count_time = 0
        #     while count_time < 10:
        #         count_time += 1
        #
        #         if fn_predicate():
        #             if not (fn_event_execution is None):
        #                 fn_event_execution()
        #             break
        #         else:
        #             fn_action()
        #
        #         sleep(second)
        #         logging.info(f'Ожидание {second * count_time}сек')
        #
        # with allure.step('Нажать кнопку "В корзину"'):
        #     wait_event(lambda: page.locator('button[value="435"]').click(),
        #                )

        with allure.step('Нажать кнопку "В корзину"'):
            page.locator('button[value="435"]').click()

            page.wait_for_event('domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()
        web_driver_wait('.cart-discount.coupon-givemehalyava')

        with allure.step('Проверяем, что купон не применился повторно'):
            total_summ_order = price_parser('tr.cart-subtotal>td>span')
            discount_summ = price_parser('tr.order-total>td span.amount')

            if discount_summ != total_summ_order:
                screenshots = str(current_path.parent.parent) + "\\screenshots\\"
                page.locator('div.woocommerce').screenshot(
                    path=screenshots + "Промокод GIVEMEHALYAVA применился повторно.png")

            assert discount_summ == total_summ_order, 'Промокод GIVEMEHALYAVA применился повторно'

    @allure.title("Зарегистрироваться в бонусной программе")
    def test_red_bonus(seif,
                       page,
                       goto_to,
                       authorization,
                       click_my_account):
        """
                            Кейс №9 - Сценарий №5
                    Предусловие: Пользователь должен быть Авторизован.
                    Шаги:
                    1. Открыть страницу http://pizzeria.skillbox.cc
                    2. Нажать на раздел в хедере страницы "Бонусная программа"
                    2.1. Ввести данные в поле имя.
                    2.2. Ввести данные в поле телефон.
                    3. Нажать кнопку "Оформить карту"

        """

        goto_to()
        click_my_account()
        authorization()

        with allure.step('Нажать на раздел в хедере страницы "Бонусная программа"'):
            page.locator('li[id="menu-item-363"] a').click()

        with allure.step('Заполнить поля имя и телефон'):
            page.locator('input[name="username"]').fill('Екатерина')
            page.locator('input[id="bonus_phone"]').fill('89095608899')

        with allure.step('Нажать кнопку "Оформить карту"'):
            page.locator('button[name="bonus"]').click()

    @allure.title("Проверить применение скидки 15% по № телефона (бонусная программа)")
    def test_check_bonus(seif,
                         page,
                         goto_to,
                         authorization,
                         click_my_account,
                         point_and_click,
                         order_date,
                         fill_order_form):
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

        goto_to()
        click_my_account()
        authorization()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            point_and_click('li[id="menu-item-391"] > a')

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            page.locator('li.post-435 a[class="collection_title"]').hover()
            page.locator('li.post-435 a[class="collection_title"]').click()

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        with allure.step('Ввести в поле- комментария номер телефона 89095608899'):
            page.locator('#order_comments').fill('89095608899')

            order_date()
            fill_order_form()

        with allure.step('Установить галочку в чек - боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

    @allure.title('Проверить валидацию полей раздела "Бонусная программа"')
    def test_checkstring_bonus(seif,
                               page,
                               goto_to,
                               authorization,
                               click_my_account):
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

        goto_to()
        click_my_account()
        authorization()

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

    string_phon = [generation_random_digits(10), generation_random_digits(11), generation_random_digits(12),
                   f' {generation_random_digits(11)} ', '', '8 921 044 23 99', '8-921-044-23-99',
                   '<script>alert(‘XSS’)</script>', generation_random_digits(255), '1', "tr'"]
