def is_element(page, selector):
    is_element = page.locator(selector).count() > 0
    return is_element

def text_contain(el, text):
    return el.inner_text().upper().find(text.upper()) != -1


def text_contain_input_value(el, text):
    return el.input_value().upper().find(text.upper()) != -1
