import logging.config
from pathlib import Path

current_path = Path(__file__)
logging_path = current_path.parent.joinpath("logging.ini")
logging.config.fileConfig(logging_path)


def pytest_addoption(parser):
    parser.addini("nameuser", "Имя пользователя")
    parser.addini("user_email", "Email пользователя")
    parser.addini("password_user", "Пароль пользователя")


pytest_plugins = [
    "src.fixtures"
]
