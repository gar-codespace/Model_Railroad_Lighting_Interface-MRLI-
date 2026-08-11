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

# DISPLAY_MODE: WELCOME
def WELCOME_turn_left():
    entities.DISPLAY_MODE = 'EFFECTS'

def WELCOME_turn_right():
    entities.DISPLAY_MODE = 'EFFECTS'

def WELCOME_get_hilight():
    # Move the hilight rectangle off the screen

    return 65

def WELCOME_click():
    entities.DISPLAY_MODE = 'EFFECTS'

# DISPLAY_MODE: EFFECTS

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

    return hilight_row

def EFFECTS_click():

    print(entities.HILIGHTED_EFFECT)
    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.DISPLAY_MODE = entities.CURRENT_EFFECT[1]
    print(entities.DISPLAY_MODE)

    return get_status_screen()

def EFFECTS_confirm_released():

    entities.DISPLAY_MODE = 'STANDBY'
    print('EFFECTS_confirm_released')

    return

# DISPLAY_MODE: STATIC

def STATIC_turn_left():
    print('STATIC_turn_left')

    row = entities.STATIC_SELECT_ROW + 1
    entities.STATIC_SELECT_ROW = min(row, 4)

def STATIC_turn_right():
    print('STATIC_turn_right')

    row = entities.STATIC_SELECT_ROW - 1
    entities.STATIC_SELECT_ROW = max(0, row)

def STATIC_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT'] - 1
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row

def STATIC_click():
    print('STATIC_click')

def STATIC_click2():
    print('STATIC_click2')
    entities.DISPLAY_MODE = 'EFFECTS'

    return get_menu_list()

# DISPLAY_MODE: ANIMATED

def ANIMATED_click():
    print('ANIMATED_click')
    # pause and play the animated effect

# DISPLAY_MODE: EDIT

def EDIT_turn_left():
    print('EDIT_turn_left')

def EDIT_turn_right():
    print('EDIT_turn_right')

def EDIT_click():
    print('EDIT_click')

# DISPLAY_MODE: STANDBY

def STANDBY_click():
    print('STANDBY_click')











 








############# OLD STUFF ################



def show_status_screen_manual(display, direction:str):
        display.fill(0)
        status_screen(display)
        manual_hilight(display, direction)
        display.show()
    
def manual_hilight(display, direction: str='None'):
    '''
    Manual hilight is only used when the machine is is manual mode.
    The min and max values can be hardcoded because there are 5 led colors and that's not changing.
    (famous last words)
    '''

    if direction == 'right':
        entities.STATUS_HILIGHT_INDEX -= 1
        entities.STATUS_HILIGHT_INDEX = max(0, entities.STATUS_HILIGHT_INDEX)

    elif direction == 'left':
        entities.STATUS_HILIGHT_INDEX += 1
        entities.STATUS_HILIGHT_INDEX = min(entities.STATUS_HILIGHT_INDEX, 4)

    x = entities.MAIN_FORMAT['LINE_HEIGHT'] * entities.STATUS_HILIGHT_INDEX
    hilight = display.rect(0, x, 128, 10, 1)

    return hilight
