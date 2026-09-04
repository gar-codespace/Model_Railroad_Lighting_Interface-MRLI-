import entities
import model


def get_display(specs):
            
    bus = specs[0]
    width = specs[1]
    height = specs[2]
    addr = specs[3]

    i2c = entities.I2C(
                        bus,
                        sda = entities.PIN(entities.PICO_PIN['SDA']),
                        scl = entities.PIN(entities.PICO_PIN['SCL']),
                        freq = 400000
                        )

    return entities.DISPLAY_LIBRARY.DRIVER_I2C(width, height, i2c, addr)

def get_menu_list() -> list:
    '''
    Returns a list of main menu items.
    '''

    index_double = model.get_index_double()
    index_subset = index_double[entities.MENU_FIRST_ITEM:]
    entities.HILIGHTED_EFFECT = index_subset[entities.HIGHLIGHT_ROW]

    menu_list: list = []
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        menu_list.append(entities.MAIN_MENU.get(index_subset[i])[0])

    return menu_list

def get_status_list() -> list:
    '''
    The status screen is displayed when the display mode is ANIMATED, STATIC, or EDIT.
    '''
    status_screen: list = []

    value = model.pwm2percent(getattr(entities, 'RED')) * 100
    status_screen.append(f'Red:   {round(value, 4)}%')

    value = model.pwm2percent(getattr(entities, 'GREEN')) * 100
    status_screen.append(f'Green: {round(value, 4)}%')

    value = model.pwm2percent(getattr(entities, 'BLUE')) * 100
    status_screen.append(f'Blue:  {round(value, 4)}%')

    value = model.pwm2percent(getattr(entities, 'WARM')) * 100
    status_screen.append(f'Warm:  {round(value, 4)}%')

    value = model.pwm2percent(getattr(entities, 'COOL')) * 100
    status_screen.append(f'Cool:  {round(value, 4)}%')

    return status_screen
