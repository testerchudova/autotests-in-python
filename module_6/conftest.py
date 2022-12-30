pytest_plugins = [
    "src.fixtures.system.browser"
]

def pytest_addoption(parser):
    parser.addini("selenium_url", "Путь к селениуму")
    parser.addini("browser_name", "Имя браузера")
    parser.addini("browser_version", "Версия браузера")