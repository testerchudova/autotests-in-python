from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


def moving_element(selenium, element, coordinates:list):
    x = coordinates[0]
    y = coordinates[1]
    ActionChains(selenium) \
        .click_and_hold(element) \
        .move_by_offset(x, y) \
        .release() \
        .perform()

def move_to_element(selenium, graf):
    ActionChains(selenium) \
        .move_to_element(graf) \
        .perform()

def pause(selenium, timeout=1):
    ActionChains(selenium).pause(timeout).perform()


def element_wait(selenium, timeout, func):
    element = WebDriverWait(selenium, timeout).until(func)
    return element