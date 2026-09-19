import entities
import model


def get_display(board, bus) -> object:

    width = board['WIDTH']
    height = board['HEIGHT']
    addr = board['ADDRESS']

    return entities.DISPLAY_DRIVER(width, height, bus, addr)

def get_welcome_list() -> list:

    welcome_list: list = []

    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        try:
            welcome_list.append(entities.WELCOME_SCREEN[i])
        except:
            welcome_list.append('')

    return welcome_list

def get_menu_list() -> list:
    '''Returns a list of main menu items.'''

    index_double = model.get_index_double()
    index_subset = index_double[entities.MENU_FIRST_ITEM:]
    entities.HILIGHTED_EFFECT = index_subset[entities.HIGHLIGHT_ROW]

    menu_list: list = []
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        menu_list.append(entities.MAIN_MENU.get(index_subset[i])[0])

    return menu_list

def get_status_list() -> list:
    '''The status screen is displayed when the machine state is ANIMATED, STATIC, or EDIT.
    TODO Hardcoding??? Yikes!!
    '''

    status_screen: list = []

    status_screen.append(f'Waypoint:{entities.WP_NAME}')

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

def get_empty_list() -> list:

    menu_list: list = []

    for _ in range(0, entities.MAIN_FORMAT['ROWS']):
            menu_list.append('')

    return menu_list