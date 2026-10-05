import entities
import model
import states


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

def get_effects_list() -> list:
    '''Returns a list of effects menu items.'''

    index_double = model.get_index_double()
    index_subset = index_double[entities.EFFECTS_MENU_FIRST_ITEM:] # it's only important to chop the beginning
    entities.EFFECTS_HILIGHTED_EFFECT = index_subset[entities.EFFECTS_HIGHLIGHT_ROW]

    menu_list: list = []
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        menu_list.append(entities.EFFECTS_MENU.get(index_subset[i])[0])

    return menu_list

def get_status_list() -> list:
    '''The status screen is displayed when the machine state is ANIMATED, STATIC, or EDIT.'''

    status_screen: list = []

    # The first line can change, depending on the machine state
    attrib = f'{entities.MACHINE_STATE}_first_line'
    first_line = getattr(states, attrib)() # IE animated_first_line()

    status_screen.append(first_line)
    
    value = model.pwm_percent(entities.RED)
    # status_screen.append(f'  Red: {value[1]}%')
    status_screen.append(f'  Red: {value:.4%}')

    value = model.pwm_percent(entities.GREEN)
    status_screen.append(f'Green: {value:.4%}')

    value = model.pwm_percent(entities.BLUE)
    status_screen.append(f' Blue: {value:.4%}')

    value = model.pwm_percent(entities.WARM)
    status_screen.append(f' Warm: {value:.4%}')

    value = model.pwm_percent(entities.COOL)
    status_screen.append(f' Cool: {value:.4%}')

    return status_screen

def get_empty_list() -> list:

    return ['' for _ in range(entities.MAIN_FORMAT['ROWS'])]