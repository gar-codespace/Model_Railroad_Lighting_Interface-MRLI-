'''
Support methods for the controls library
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
    
    
def welcome_screen(display):
    '''
    Only displayed on start up,
    '''

    line_y = 0
    for i in range(entities.MAIN_FORMAT['ROWS']):
        display.text(entities.WELCOME_SCREEN[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
        line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

    return

def routine_screen(display):
    '''
    The routine screen is displayed when the machine is in routine mode.
    This is where the user selects which routine to run.
    '''
    
    x = entities.MAIN_FORMAT['X_OFFSET']
    y = 1
    index = model.get_menu_index()
    entities.SCROLL_ROUTINE = index[2]
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        routine = entities.ROUTINES[index[i]]
        routine = getattr(entities, routine, 'DAY')['name']
        display.text(routine, x, y)
        y += entities.MAIN_FORMAT['LINE_HEIGHT']

    display.rect(0, 26, 128, 10, 1)

    return

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

def manual_hilight(display, direction: str):
    '''
    Manual hilight is only used when the machine is is manual mode.
    The min and max values can be hardcoded because there are 5 led colors and that's not changing
    (famous last words)
    '''

    if direction == 'RIGHT':
        entities.STATUS_HILIGHT_INDEX -= 1
        entities.STATUS_HILIGHT_INDEX = max(0, entities.STATUS_HILIGHT_INDEX)

    if direction == 'LEFT':
        entities.STATUS_HILIGHT_INDEX += 1
        entities.STATUS_HILIGHT_INDEX = min(entities.STATUS_HILIGHT_INDEX, 4)

    x = entities.MAIN_FORMAT['LINE_HEIGHT'] * entities.STATUS_HILIGHT_INDEX
    hilight = display.rect(0, x, 128, 10, 1)

    return hilight

def adjust_color_value(direction: str): # move to model?

    color_being_adjusted = entities.LED_INDEX_MAP[entities.STATUS_HILIGHT_INDEX]
    pwm_color_value = entities.PWM_VALUES[color_being_adjusted]

    if direction == 'RIGHT': # turn it up
        pwm_color_value += entities.PWM_TICKS
        pwm_color_value = min(pwm_color_value, entities.PWM_STEPS)
        entities.PWM_VALUES[color_being_adjusted] = pwm_color_value

    if direction == 'LEFT': # turn it down
        pwm_color_value -= entities.PWM_TICKS
        pwm_color_value = max(0, pwm_color_value)
        entities.PWM_VALUES[color_being_adjusted] = pwm_color_value
