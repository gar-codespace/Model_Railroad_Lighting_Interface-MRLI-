'''
Support methods for the controls library
Everything is here that involves the OLED display.
'''

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

    return entities.SSD1306_I2C(width, height, i2c, addr)


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

    value = model.pwm2percent(entities.PWM_VALUES['RED'])
    status_screen.append(f'Red:   {value}%')

    value = model.pwm2percent(entities.PWM_VALUES['GREEN'])
    status_screen.append(f'Green: {value}%')

    value = model.pwm2percent(entities.PWM_VALUES['BLUE'])
    status_screen.append(f'Blue:  {value}%')

    value = model.pwm2percent(entities.PWM_VALUES['WARM'])
    status_screen.append(f'Warm:  {value}%')

    value = model.pwm2percent(entities.PWM_VALUES['COOL'])
    status_screen.append(f'Cool:  {value}%')

    return status_screen


########### DISPLAY_MODE: WELCOME


def WELCOME_turn_left():
    entities.DISPLAY_MODE = 'EFFECTS'

def WELCOME_turn_right():
    entities.DISPLAY_MODE = 'EFFECTS'

def WELCOME_get_hilight():
    # Move the hilight rectangle off the screen

    return 65

def WELCOME_click():
    entities.DISPLAY_MODE = 'EFFECTS'


########### DISPLAY_MODE: EFFECTS


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

def EFFECTS_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT'] - 1
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height

    return hilight_row + 1

def EFFECTS_click():

    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.DISPLAY_MODE = entities.CURRENT_EFFECT[1]

    return get_status_screen()

def EFFECTS_confirm_released():

    entities.DISPLAY_MODE = 'STANDBY'
    print('EFFECTS_confirm_released')

    return


########### DISPLAY_MODE: STATIC


def STATIC_turn_left():

    row = entities.STATIC_SELECT_ROW + 1
    entities.STATIC_SELECT_ROW = min(row, 4)

    return get_status_screen()

def STATIC_turn_right():

    row = entities.STATIC_SELECT_ROW - 1
    entities.STATIC_SELECT_ROW = max(0, row)

    return get_status_screen()

def STATIC_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1

def STATIC_click():

    entities.DISPLAY_MODE = 'EDIT'

def STATIC_click2():
    
    entities.DISPLAY_MODE = 'EFFECTS'

    return get_menu_list()


########### DISPLAY_MODE: ANIMATED


def ANIMATED_click():
    print('ANIMATED_click')
    # pause and play the animated effect

def ANIMATED_click2():
    
    entities.DISPLAY_MODE = 'EFFECTS'

    return get_menu_list()


########### DISPLAY_MODE: EDIT


def EDIT_turn_left():

    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]
    pwm_value = entities.PWM_VALUES.get(color)

    pwm_value -= entities.PWM_TICKS
    pwm_value = max(0, pwm_value)

    entities.PWM_VALUES[color] = pwm_value

    return get_status_screen()

def EDIT_turn_right():

    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]
    pwm_value = entities.PWM_VALUES.get(color)

    pwm_value += entities.PWM_TICKS
    pwm_value = min(pwm_value, entities.PWM_STEPS)

    entities.PWM_VALUES[color] = pwm_value

    return get_status_screen()

def EDIT_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1

def EDIT_click():

    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.DISPLAY_MODE = entities.CURRENT_EFFECT[1]

    return get_status_screen()

def EDIT_click2():

    entities.DISPLAY_MODE = 'EFFECTS'

    return get_menu_list()


########### DISPLAY_MODE: STANDBY
