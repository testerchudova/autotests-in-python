import logging.config
from pathlib import Path
current_path = Path(__file__)
logging_path = current_path.parent.joinpath("logging.ini")

logging.config.fileConfig(logging_path)



pytest_plugins = [
    "src.fixtures"
]

def pytest_addoption(parser):
    parser.addini("selenium_url", "Путь к селениуму")
    parser.addini("browser_name", "Имя браузера")
    parser.addini("browser_version", "Версия браузера")