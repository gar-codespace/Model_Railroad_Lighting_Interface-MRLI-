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

def get_status_screen() -> list:
    '''
    The status screen is displayed when the display mode is ANIMATED, STATIC, or EDIT.
    '''
    status_screen: list = []

    value = model.pwm2percent(getattr(entities, 'RED')) * 100
    status_screen.append(f'Red:   {round(value, 2)}%')

    value = model.pwm2percent(getattr(entities, 'GREEN')) * 100
    status_screen.append(f'Green: {round(value, 2)}%')

    value = model.pwm2percent(getattr(entities, 'BLUE')) * 100
    status_screen.append(f'Blue:  {round(value, 2)}%')

    value = model.pwm2percent(getattr(entities, 'WARM')) * 100
    status_screen.append(f'Warm:  {round(value, 2)}%')

    value = model.pwm2percent(getattr(entities, 'COOL')) * 100
    status_screen.append(f'Cool:  {round(value, 2)}%')

    return status_screen


########### DISPLAY_STATE: WELCOME


def WELCOME_turn_left():
    entities.DISPLAY_STATE = 'EFFECTS'

    return get_menu_list()

def WELCOME_turn_right():
    entities.DISPLAY_STATE = 'EFFECTS'

    return get_menu_list()

def WELCOME_click():
    entities.DISPLAY_STATE = 'EFFECTS'

    return get_menu_list()

def WELCOME_get_hilight():
    # Move the hilight rectangle off the screen

    return 65


########### DISPLAY_STATE: EFFECTS


def EFFECTS_turn_left():
    '''
    This is the menu of available EFFECTS.
    '''
    entities.MENU_FIRST_ITEM -= 1
    if entities.MENU_FIRST_ITEM < 0:
        entities.MENU_FIRST_ITEM = len(entities.MAIN_MENU) - 1

    return get_menu_list()

def EFFECTS_turn_right():
    '''
    This is the menu of available EFFECTS.
    '''
    entities.MENU_FIRST_ITEM += 1
    if entities.MENU_FIRST_ITEM > len(entities.MAIN_MENU) - 1:
        entities.MENU_FIRST_ITEM = 0

    return get_menu_list()

def EFFECTS_click():

    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.DISPLAY_STATE = 'STATIC'
    if not entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.DISPLAY_STATE = 'ANIMATED'

    return get_status_screen()

def EFFECTS_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT'] - 1
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height

    return hilight_row + 1


########### DISPLAY_STATE: ANIMATED


def ANIMATED_click():

    if entities.DISPLAY_STATE == 'PAUSED':
        entities.DISPLAY_STATE = 'ANIMATED'
    else:
        entities.DISPLAY_STATE = 'PAUSED'

    return get_menu_list()

def ANIMATED_click2():
    
    entities.DISPLAY_STATE = 'EFFECTS'

    return get_menu_list()


########### DISPLAY_STATE: STATIC


def STATIC_turn_left():

    row = entities.STATIC_SELECT_ROW + 1
    entities.STATIC_SELECT_ROW = min(row, 4)

    return get_status_screen()

def STATIC_turn_right():

    row = entities.STATIC_SELECT_ROW - 1
    entities.STATIC_SELECT_ROW = max(0, row)

    return get_status_screen()

def STATIC_click():

    entities.DISPLAY_STATE = 'EDIT'

    return get_status_screen()

def STATIC_click2():
    
    entities.DISPLAY_STATE = 'EFFECTS'

    return get_menu_list()

def STATIC_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1



########### DISPLAY_STATE: EDIT


def EDIT_turn_left():

    index = entities.CURRENT_EFFECT[2]
    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]

    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value -= entities.PWM_TICKS # PWM expression
    pwm_color_value = max(pwm_color_value, 0) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.STATIC_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER


    return get_status_screen()

def EDIT_turn_right():
    
    index = entities.CURRENT_EFFECT[2]
    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]
    
    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value += entities.PWM_TICKS # PWM expression
    pwm_color_value = min(pwm_color_value, entities.PWM_STEPS) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.STATIC_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER

    return get_status_screen()

def EDIT_click():

    entities.DISPLAY_STATE = 'STATIC'

    return get_status_screen()

def EDIT_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1
