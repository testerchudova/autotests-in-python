def is_element(common_by, selector, selenium):
    is_element = len(selenium.find_elements(common_by, selector)) > 0
    return is_element
