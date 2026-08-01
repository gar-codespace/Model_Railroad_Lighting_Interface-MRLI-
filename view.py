'''
Support methods for the controls library
Everything is here that involves the OLED display.
'''

import entities
import model


class Display():

    def __init__(self, specs):

        self.bus = specs[0]
        self.width = specs[1]
        self.height = specs[2]
        self.addr = specs[3]

    def getDisplay(self):

        i2c = entities.I2C(
                        self.bus,
                        sda = entities.PIN(entities.PICO_PIN['SDA']),
                        scl = entities.PIN(entities.PICO_PIN['SCL']),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)
    
def show_blank_screen(display):
    
    display.fill(0)
    display.show()

def welcome_screen(display):
    '''
    Only displayed on start up,
    '''

    line_y = 0
    for i in range(entities.MAIN_FORMAT['ROWS']):
        display.text(entities.WELCOME_SCREEN[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
        line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

    return

def show_welcome_screen(display):
    display.fill(0)
    welcome_screen(display)
    display.show()

def effect_screen(display):
    '''
    The effect screen is displayed when the machine is in AUTOMATIC mode.
    This is where the user selects which effect to run.
    '''

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height
    x = entities.MAIN_FORMAT['X_OFFSET']
    y = 1
    index = model.get_menu_index()
    entities.SCROLL_EFFECT = index[0]
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        effect = entities.EFFECTS[index[i]]
        effect = getattr(entities, effect, 'DAY')['name']
        display.text(effect, x, y)
        y += entities.MAIN_FORMAT['LINE_HEIGHT']

    display.rect(0, hilight_row, 128, 10, 1)

    return

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
