from time import sleep
import allure
from pprint import pprint
import pytest
from final_work.src.Utils.сhecking_elements import *  # noqa
from final_work.src.actions.actions import *  # noqa
from final_work.src.fixtures import Actions


class TestExample(Actions):

    @allure.title("Кейс №1 Регистрация пользователя")
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

        logging.info('запуск теста test_user_registration')
        goto_to()

        logging.info('Клик по меню "Мой аккаунт"')
        click_my_account()

        user_registration(nameuser='testnameuser25', user_email='testnameuser25@bk.ru', password_user='testnameuser25')

    @allure.title("Кейс №2 Оформление заказа пиццы")
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

        logging.info('запуск теста test_order_pizza')
        goto_to()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=417"]')

        logging.info('Клик по меню "Мой аккаунт"')
        click_my_account()

        logging.info('Заполнение формы "авторизация пользователя"')
        authorization()

        with allure.step('Нажать на иконку "Корзина" в правом верхнем углу сайта.'):
            page.locator('a[class="cart-contents wcmenucart-contents"]').click()

        with allure.step('Нажать на кнопку "Перейти к оплате"'):
            page.locator('a[class="checkout-button button alt wc-forward"]').click()

        fill_order_form()
        order_date()

        with allure.step('Выбрать способ оплаты radio-button: "Оплата при доставке"'):
            page.locator('#payment_method_cod').click()

        with allure.step('Установить галочку в чек- боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

            click_my_account()
            page.wait_for_event('domcontentloaded')

        with allure.step('Нажать кнопку "Заказы"'):
            orders = page.locator(
                'li[class="woocommerce-MyAccount-navigation-link woocommerce-MyAccount-navigation-link--orders"] a')
            orders.click()

        with allure.step('Нажать кнопку подробнее'):
            orders = page.locator('div.woocommerce-MyAccount-content tbody tr:first-child td:last-child a.view')
            orders.click()

        with allure.step('Проверка результата нажатия кнопки'):
            assert is_element(page, '.order-date'), "При нажатии кнопки действие не произошло"

    @allure.title("Кейс №3 Редактирование заказа")
    def test_order_edit(seif,
                        page,
                        goto_to,
                        authorization,
                        click_on_main,
                        click_my_account,
                        point_and_click):
        """
                Кейс №3
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

    @allure.title("Кейс №4 Применение промокода при оформлении заказа.")
    def test_order_coupon(seif,
                          page,
                          goto_to,
                          authorization,
                          click_on_main,
                          click_my_account,
                          point_and_click,
                          coupon_entry,
                          price_parser,
                          checking_discount,
                          screenshot_el):
        """
           Кейс №4 - Сценарий №1
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
            page.wait_for_event('domcontentloaded')

        coupon_entry()

        with allure.step('Убедится, что сумма заказа уменьшилась на 10%'):
            percent = 10
            checking_coupon_discount = checking_discount(percent_discount=percent)

        if not checking_coupon_discount:
            screenshot_el(name_files=f'Сумма скидки не равна {percent}%.png',
                          selector='div.woocommerce')

        assert checking_coupon_discount, f"Сумма скидки не равна {percent}%"

    @allure.title("Кейс №5 Применение невалидного промокода при оформлении заказа.")
    def test_order_wrongcoupon(seif,
                               page,
                               goto_to,
                               authorization,
                               click_on_main,
                               click_my_account,
                               point_and_click,
                               coupon_entry,
                               price_parser,
                               checking_discount,
                               screenshot_el,
                               clear_trash):

        """
              Кейс №5 - Сценарий №2
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
        coupon = 'DC120'
        goto_to()
        click_my_account()
        authorization()
        clear_trash()
        click_on_main()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Пепперони и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=417"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()
            page.wait_for_event('domcontentloaded')

        coupon_entry(name_coupon=coupon)

        with allure.step(f'Проверяем, что купон {coupon} не применился'):
            checking_coupon_discount = checking_discount(percent_discount=0)

            if not checking_coupon_discount:
                screenshot_el(name_files=f"Скидка при невалидном купоне {coupon}.png", selector='div.woocommerce')

            assert checking_coupon_discount, 'Пользователь получил скидку в результате применения невалидного купона'

    @allure.title("Кейс №6 Перехватить промокод GIVEMEHALYAVA.")
    def test_order_block_coupon(seif,
                                page,
                                goto_to,
                                authorization,
                                click_on_main,
                                click_my_account,
                                point_and_click,
                                coupon_entry,
                                price_parser,
                                checking_discount,
                                screenshot_el,
                                web_driver_wait,
                                clear_trash):

        """
                Кейс №6 - Сценарий №3
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

        coupon = 'GIVEMEHALYAVA'

        goto_to()
        click_my_account()
        authorization()
        pytest.fixture()
        clear_trash()

        click_on_main()

        with allure.step('Выбрать пиццу и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('В слайдере "Пиццы" нажать на стрелку - Вправо'):
            point_and_click('a[class="slick-next"]')

        with allure.step('Выбрать пиццу Рай и Нажать на кнопку -В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=421"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()
            page.wait_for_event('domcontentloaded')

        page.route("http://pizzeria.skillbox.cc/?wc-ajax=apply_coupon", lambda route: route.fulfill(status=500))
        coupon_entry()

        with allure.step(f'Проверяем, что купон {coupon} не применился в результате ответа сервера "status=500"'):
            checking_coupon_discount = checking_discount(percent_discount=0)

        if not checking_coupon_discount:
            screenshot_el(name_files=f'купон {coupon} не применился в результате ответа сервера status=500.png',
                          selector='div.woocommerce')

        assert checking_coupon_discount, f'{coupon} Купон применился в результате ответа сервера "status=500"'

    @allure.title("Кейс №7 Применение промокода ПОВТОРНО при оформлении заказа.")
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
                                   web_driver_wait,
                                   checking_discount,
                                   screenshot_el):

        """
            Кейс №7 - Сценарий №4
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
        coupon = 'GIVEMEHALYAVA'

        goto_to()
        click_my_account()
        user_registration(nameuser=nameuser, user_email=user_email, password_user=password_user)
        click_on_main()

        with allure.step('Выбрать пиццу "Пицца 4 в 1" и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=425"]')

        with allure.step('Выбрать пиццу "Рай" и нажать - В корзину'):
            point_and_click('li[aria-hidden="false"] a[href="?add-to-cart=421"]')

        with allure.step('Нажать на раздел в хедере страницы "Оформлениe заказа"'):
            page.locator('li[id="menu-item-31"] a').click()
            page.wait_for_event('domcontentloaded')

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

        with allure.step('Нажать кнопку "В корзину"'):
            page.locator('button[value="435"]').click()

        page.wait_for_event('domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        coupon_entry()
        web_driver_wait('.cart-discount.coupon-givemehalyava')

        with allure.step('Проверяем, что купон не применился повторно'):
            checking_coupon_discount = checking_discount(percent_discount=10)

            if checking_coupon_discount:
                screenshot_el(name_files=f"Промокод {coupon} применился повторно.png", selector='div.woocommerce')

            assert not checking_coupon_discount, f"Промокод {coupon} применился повторно.png"

    @allure.title("Кейс №8 Зарегистрироваться в бонусной программе")
    def test_red_bonus(seif,
                       page,
                       goto_to,
                       authorization,
                       click_my_account,
                       pytestconfig):
        """
            Кейс №8 - Сценарий №5
            Шаги:
            1. Открыть страницу http://pizzeria.skillbox.cc
            2. Нажать на раздел в хедере страницы "Бонусная программа"
            2.1. Ввести данные в поле имя.
            2.2. Ввести данные в поле телефон.
            3. Нажать кнопку "Оформить карту"
        """
        telephone = pytestconfig.getini('telephone')
        goto_to()
        click_my_account()
        authorization()

        with allure.step('Нажать на раздел в хедере страницы "Бонусная программа"'):
            page.locator('li[id="menu-item-363"] a').click()

        with allure.step(f'Заполнить поля имя и телефон {telephone}'):
            page.locator('input[name="username"]').fill('Екатерина')
            page.locator('input[id="bonus_phone"]').fill(telephone)

        with allure.step('Нажать кнопку "Оформить карту"'):
            page.locator('button[name="bonus"]').click()

        with allure.step('Проверка оформления карты'):
            assert is_element(page, 'div#bonus_main>h3'), "Бонусная карта не оформлена"

    @allure.title("Кейс №9 Проверить применение скидки 15% по № телефона (бонусная программа)")
    def test_check_bonus(seif,
                         page,
                         goto_to,
                         authorization,
                         click_my_account,
                         point_and_click,
                         order_date,
                         fill_order_form,
                         price_parser,
                         pytestconfig,
                         screenshot_el,
                         clear_trash):

        """
            Кейс №9- Сценарий №6
            1.	Открыть страницу http://pizzeria.skillbox.cc
            2.	Кликнуть пункт меню "Мой аккаунт"
            3.	Провести авторизацию пользователя
            4.	Выбрать подкатегорию в "Меню" -"Десерты".
            5.	Нажать подкатегорию "Меню" -"Десерты"
            6.	Нажать на иконку десерта "Шоколадный шок"
            7.	Нажать на кнопку "В корзину".
            8.	Нажать на раздел в хедере страницы "Оформление заказа"
            9.	Нажать на поле- ссылку для открытия поля- ввода купона.
            10.	Ввести в поле- комментария номер телефона '89095608899'.
            11.	До заполнить на странице "Оформление заказа" обязательные поля,
                не заполненные по умолчанию: дата заказа.
            12.	Установить галочку в чек- боксе согласия с условиями вебсайта.
            13.	Нажать кнопку "Оформить заказ"
            14.	Убедиться, что применилась скидка 15%
        """
        telephone = pytestconfig.getini('telephone')
        goto_to()
        click_my_account()
        authorization()
        clear_trash()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            page.locator('li[id="menu-item-389"] > a').hover()

        with allure.step('Выбрать подкатегорию в "Меню" -"Десерты".'):
            point_and_click('li[id="menu-item-391"] > a')

        with allure.step('Нажать на иконку десерта "Шоколадный шок".'):
            point_and_click('li.post-435 a[class="collection_title"]')

        page.wait_for_event('domcontentloaded')

        with allure.step('Нажать кнопку "В корзину"'):
            page.locator('button[value="435"]').click()

        page.wait_for_event('domcontentloaded')

        with allure.step('Нажать на раздел в хедере страницы "Оформлени заказа"'):
            page.locator('li[id="menu-item-31"] a').click()

        with allure.step(f'Ввести в поле- комментария номер телефона {telephone}'):
            page.locator('#order_comments').fill(telephone)

            order_date()
            fill_order_form()

        with allure.step('Установить галочку в чек - боксе согласия с условиями вебсайта.'):
            page.locator('#terms').click()

        with allure.step('Нажать кнопку "Оформить заказ"'):
            page.locator('#place_order').click()

        page.wait_for_event('domcontentloaded')

        with allure.step(f'Проверяем применение скидки 15% по № {telephone}'):
            percent = 15
            discount = percent / 100
            total = price_parser('tfoot>tr:nth-of-type(3) .amount')
            subtotal = price_parser('tfoot>tr:nth-of-type(1) .amount')

            if total * (1 - discount) != subtotal:
                screenshot_el(name_files=f'Cкидкa 15% по № {telephone} не применилась.png',
                              selector='div.woocommerce')

            assert total * (1 - discount) == subtotal, f'Cкидкa 15% по № {telephone} не применилась'

    @allure.title('Кейс №10 Проверить валидацию полей раздела "Бонусная программа"')
    def test_check_form_bonus_program(seif,
                                      page,
                                      goto_to,
                                      authorization,
                                      click_my_account,
                                      pytestconfig,
                                      web_driver_wait):
        """
        Кейс №10- Сценарий №6
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

        string_user = ['',
                       ' Катя ',
                       '`~@#$%^&*()_+|-=\{}[]:',
                       'ТАНЯ',
                       '<script>alert(‘XSS’)</script>',
                       generation_random_digits(10),
                       generation_random_string(255)]

        string_phon = [generation_random_digits(10),
                       generation_random_digits(11),
                       generation_random_digits(12),
                       f' {generation_random_digits(11)} ',
                       '',
                       '8 921 044 23 99',
                       '8-921-044-23-99',
                       '<script>alert(‘XSS’)</script>',
                       generation_random_digits(255),
                       '1',
                       "tr'"]
        inputs = [[page.locator('input[name="username"]'), 'Екатерина', string_user, 'Имя пользователя'],
                  [page.locator('input[id="bonus_phone"]'), pytestconfig.getini('telephone'), string_phon,
                   'Телефон пользователя']
                  ]

        def clear(inputs):
            for item_inputs in inputs:
                item_inputs[0].clear()

        def fill(inputs):
            for item_inputs in inputs:
                item_inputs[0].fill(item_inputs[1])

        def predicate():
            """
            Возвращает результат проверки, отработала ли форма с невалидным значением
            :return: bool
            """
            page.keyboard.press('Enter')
            return not is_element(page, 'input#bonus_username', timeout=1000)

        test_err = []

        def save_inputs_value(inputs):
            """
            Сохраняет имена и значения всех полей
            """
            res = []
            for item in inputs:
                res += [item[3], item[1]]

            test_err.append(res)

        def click_section_bonus_program():
            web_driver_wait('li[id="menu-item-363"] a').click()

        with allure.step('Нажать на раздел в хедере страницы "Бонусная программа"'):
            click_section_bonus_program()

        for item_inputs in inputs:
            normal_value = item_inputs[1]
            for item_checked_value in item_inputs[2]:
                item_inputs[1] = item_checked_value
                fill(inputs)  # Заполняю поля данными
                sleep(1.5)

                with allure.step('Нажать кнопку "Оформить карту"'):
                    page.locator('button[name="bonus"]').click()

                if predicate():
                    save_inputs_value(inputs)
                    click_section_bonus_program()
                else:
                    clear(inputs)

            item_inputs[1] = normal_value

        assert len(test_err) == 0, f'Поля формы "БОНУСНАЯ ПРОГРАММА", возможно заполнить невалидными значениями {test_err}'
        #pprint(test_err)
