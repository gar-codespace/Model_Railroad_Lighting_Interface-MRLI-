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

# Encoder Rotation
def welcome_turn_left():
    entities.SCREEN_MODE = 'effects'

def welcome_turn_right():
    entities.SCREEN_MODE = 'effects'

def effects_turn_left():
    '''
    This is the menu of available effects.
    '''
    entities.MENU_FIRST_ITEM -= 1
    if entities.MENU_FIRST_ITEM < 0:
        entities.MENU_FIRST_ITEM = len(entities.MAIN_MENU) - 1

    return get_menu_list()

def effects_turn_right():
    '''
    This is the menu of available effects.
    '''
    entities.MENU_FIRST_ITEM += 1
    if entities.MENU_FIRST_ITEM > len(entities.MAIN_MENU) - 1:
        entities.MENU_FIRST_ITEM = 0

    return get_menu_list()

def static_turn_left():
    print('static_turn_left')

def static_turn_right():
    print('static_turn_right')

def edit_turn_left():
    print('edit_turn_left')

def edit_turn_right():
    print('edit_turn_right')

# Hilight rectangle
def welcome_get_hilight():
    # Move the hilight rectangle off the screen

    return 65

def effects_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT'] - 1
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height

    return hilight_row


# Encoder single click
def welcome_click():
    entities.SCREEN_MODE = 'effects'











############# OLD STUFF ################

def show_effects_screen(display):
    display.fill(0)
    effect_screen(display)
    display.show()

def status_screen(display):
    '''
    The status screen is displayed when the machine is in monitor or manual mode.
    '''

    x = entities.MAIN_FORMAT['X_OFFSET']
    y = 1

    value = model.pwm2percent(entities.PWM_VALUES['RED'])
    display.text(f'Red:   {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

    value = model.pwm2percent(entities.PWM_VALUES['GREEN'])
    display.text(f'Green: {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

    value = model.pwm2percent(entities.PWM_VALUES['BLUE'])
    display.text(f'Blue:  {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

    value = model.pwm2percent(entities.PWM_VALUES['WARM'])
    display.text(f'Warm:  {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

    value = model.pwm2percent(entities.PWM_VALUES['COOL'])
    display.text(f'Cool:  {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

def show_status_screen(display):
    display.fill(0)
    status_screen(display)
    display.show()

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
