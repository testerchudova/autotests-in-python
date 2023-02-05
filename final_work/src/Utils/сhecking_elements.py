import secrets
import string
from playwright._impl._api_types import TimeoutError


def generation_random_symbols(symbols: list, length):
    """
    Генирирует случайную последовательность из элементов symbols длинной length.
    :param symbols: последовательность содержащая символы, используемые для генирации строки.
    :param length: определяет длинну генерируемой строки
    :return:string возвращает строку символов длинной length
    """
    character_sequence = ''.join(secrets.choice(symbols) for i in range(length))
    return character_sequence


def generation_random_string(length):
    """
     Генирирует случайную последовательность из букв латиница, длинной length, верхний и нижний регистр.
    :param length: определяет длинну генерируемой строки
    :return: строку символов длинной length
    """
    letters = string.ascii_letters + string.ascii_uppercase
    return generation_random_symbols(letters, length)


def generation_random_digits(length):
    """
     Генирирует случайную последовательность из цыфр, длинной length.
    :param length: определяет длинну генерируемой строки
    :return: строку символов(цыфр) длинной length
    """
    digits = string.digits
    return generation_random_symbols(digits, length)


def generation_random_hieroglyph(length):
    """
     Генирирует случайную последовательность из иероглифов, длинной length.
    :param length: определяет длинну генерируемой строки
    :return: строку символов(иероглифов) длинной length
    """
    hieroglyph = '表昔龙石各守交枝具刻邑次瓦赤穴州周委協見担曲婦豸羽艮司危寺立府玄' \
                 '券参宝釆页的受乳武宅印呼玉艸在自岸令非老甩述実甲河波法皮糸由成宇白鸟' \
                 '虫虍麦舌申网定固制聿取甘妻宙幸巻缶岩龟承禸直存放生襾供豕共治舟身衣全' \
                 '泣貝耒官耳再刷矛走向果目玊若舛効考用念版电苦式机並長西居足酉羊性灰肉' \
                 '血瓜季臼件拝届毒里至禾米而争枚招行卒因角板底田祭採済捨宿'

    return generation_random_symbols(hieroglyph, length)


def generation_random_string_ru(length):
    """
     Генирирует случайную последовательность из букв кирилица, длинной length, верхний и нижний регистр.
    :param length: определяет длинну генерируемой строки
    :return: строку символов длинной length
    """

    a = ord('а')
    string_ru = ''.join([chr(i) for i in range(a, a + 32)])
    string_ru += string_ru.upper()
    return generation_random_symbols(string_ru, length)


def is_element(page, selector, timeout=30000):
    try:
        res = page.wait_for_selector(selector, timeout=timeout).is_visible()
    except TimeoutError:
        res = False
    return res


def text_contain(el, text):
    return el.inner_text().upper().find(text.upper()) != -1


def text_contain_input_value(el, text):
    return el.input_value().upper().find(text.upper()) != -1


def prefix_zero(n: int):
    """
    функция дописывает ноль перед чеслом n, если n<10
    :param n: целое число
    :return: строка
    """
    n_str = str(n)
    return "0" + n_str if n < 10 else n_str
