from selenium.webdriver import ActionChains

def moving_element(selenium, element, coordinates:list):
    x = list[0]
    y = list[1]
    ActionChains(selenium) \
        .click_and_hold(element) \
        .move_by_offset(x, y) \
        .release() \
        .perform()