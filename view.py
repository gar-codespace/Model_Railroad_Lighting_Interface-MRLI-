'''
Model Railroad Lighting Interface (MRLI)

specs:
MAIN_DISPLAY = {
            'COM':'I2C0',
            'PARAMS':'OLED0',
            'DRIVER':'DISPLAY_DRIVER0'
            }
I2C0 = {
          'TYPE':'i2c',
          'ID':0,
          'SDA':'COM0',
          'SCL':'COM1',
          'FREQ':400000
        }
OLED0 = {
        'NAME':'Main Display',
        'MAKE':'GODIYMODULES',
        'MODEL':'White OLED Display Screen',
        'SIZE':'1.3 inch',
        'BUS':'i2c',
        'CONTROLLER':'sh1106',
        'INTREGATION':'1 EC11, 2 push',
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        'ROTATE': False,
        'EXTERNAL_VCC':False,
        }
'''

import entities
import model
import states


class Display:

    def __init__(self, specs:dict):

        self.com = getattr(entities, specs['COM'])
        self.driver = getattr(entities, specs['DRIVER'])
        self.params = getattr(entities, specs['PARAMS'])

        self.bus:object = None
        self.display:object = None

    def get_bus(self):

        attr = f'get_{self.com['TYPE']}'
        self.bus = getattr(model, attr)(self.com)

    def get_display(self):

        self.display = self.driver(params=self.params, bus=self.bus)
        
    def update_display(self, content:list = None):

        self.display.fill(0)
        self.display.contrast(entities.MAIN_DISPLAY_BRIGHT)

        line_y = 3 # vertically center the text in the display
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = f'{entities.MACHINE_STATE}_get_hilight'
            h = getattr(states, attrib)()
            self.display.rect(0, h, 128, 12, 1)
        except:
            pass

        self.display.show()


def get_welcome_list() -> list:

    welcome_list: list = []
    char_per_row = entities.MAIN_FORMAT['CHAR_PER_ROW']
    line_format = f'^{char_per_row}s'

    for i in range(entities.MAIN_FORMAT['ROWS']):
        try:
            welcome_list.append(f'{entities.WELCOME_SCREEN[i]:{line_format}}')
        except:
            welcome_list.append('')

    return welcome_list

def get_effects_list() -> list:
    '''Returns a list of effects menu items.'''

    index_double = model.get_index_double()
    index_subset = index_double[entities.EFFECTS_MENU_FIRST_ITEM:] # it's only important to chop the beginning
    entities.EFFECTS_HILIGHTED_EFFECT = index_subset[entities.EFFECTS_HIGHLIGHT_ROW]

    menu_list: list = []
    for i in range(entities.MAIN_FORMAT['ROWS']):
        line_prefix = entities.EFFECTS_MENU_ANIMATED_SYMBOL
        if entities.EFFECTS_MENU.get(index_subset[i])[1] == 'STATIC':
            line_prefix = entities.EFFECTS_MENU_STATIC_SYMBOL
        line = f'{line_prefix} {entities.EFFECTS_MENU.get(index_subset[i])[0]}'
        menu_list.append(line)

    return menu_list

def get_status_list() -> list:
    '''The status screen is displayed when the machine state is ANIMATED, STATIC, or EDIT.'''

    status_screen: list = []

    # The first line can change, depending on the machine state
    attrib = f'{entities.MACHINE_STATE}_first_line'
    first_line = getattr(states, attrib)() # IE animated_first_line()

    status_screen.append(first_line)
    
    value = model.pwm_percent(entities.RED)
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

def put_progress_message():
    '''Write machine progress somewhere, screen, log, Etc.'''

    if entities.PROGRESS_MESSAGE:
        print(entities.PROGRESS_MESSAGE)
    entities.PROGRESS_MESSAGE = None
