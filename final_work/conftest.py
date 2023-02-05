import logging.config
from pathlib import Path

current_path = Path(__file__)
logging_path = current_path.parent.joinpath("logging.ini")
# logging.config.fileConfig(logging_path)
logging.config.fileConfig('D:\\Ekaterina\\autotests-in-python\\final_work\\logging.ini')


def pytest_addoption(parser):
    parser.addini("nameuser", "Имя пользователя")
    parser.addini("user_email", "Email пользователя")
    parser.addini("password_user", "Пароль пользователя")
    parser.addini("telephone", "Номер телефона пользователя")
    parser.addini("first_name", "Имя пользователя для доставки")
    parser.addini("last_name", "Фамилия пользователя для доставки")
    parser.addini("address", "Адрес пользователя для доставки")
    parser.addini("city", "Город пользователя для доставки")
    parser.addini("state", "Область пользователя для доставки")
    parser.addini("postcode", "Индекс почтовый для доставки")


pytest_plugins = [
    "src.fixtures"
]
