from selenium.webdriver import ActionChains

def moving_element(selenium, element, coordinates:list):
    x = coordinates[0]
    y = coordinates[1]
    ActionChains(selenium) \
        .click_and_hold(element) \
        .move_by_offset(x, y) \
        .release() \
        .perform()