import logging


def moving_element(page, element, coordinates: list):
    x = coordinates[0]
    y = coordinates[1]
    logging.info(f'Перемещение указателя мыши по координатам x = {x}, y = {y}')
    element.hover()
    page.mouse.down()
    page.mouse.move(x, y)
    page.mouse.up()
