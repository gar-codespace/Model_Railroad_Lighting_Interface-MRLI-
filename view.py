import entities
import model
import states


class Display:

    def __init__(self, I2C):

        self.i2c = I2C

    def get_main_display(self):

        width = entities.MAIN_DISPLAY['WIDTH']
        height = entities.MAIN_DISPLAY['HEIGHT']
        addr = entities.MAIN_DISPLAY['ADDRESS']
        self.main_display = entities.DISPLAY_DRIVER(width, height, self.i2c, addr)

    def update_main_display(self, content: list = entities.WELCOME_SCREEN):

        self.main_display.fill(0)
        self.main_display.contrast(entities.MDB)

        line_y = 3 # vertically center the text in the display
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.main_display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = f'{entities.MACHINE_STATE}_get_hilight'
            h = getattr(states, attrib)()
            self.main_display.rect(0, h, 128, 12, 1)
        except:
            pass

        self.main_display.show()


def get_welcome_list() -> list:

    welcome_list: list = []
    line_format = f'^{entities.MAIN_DISPLAY_LENGTH}s'

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
    for i in range(0, entities.MAIN_FORMAT['ROWS']):
        line_prefix = entities.EFFECTS_MENU_ANIMATED_SYMBOL
        if entities.EFFECTS_MENU.get(index_subset[i])[1] == 'STATIC':
            line_prefix = entities.EFFECTS_MENU_STATIC_SYMBOL
        line = f'{line_prefix} {entities.EFFECTS_MENU.get(index_subset[i])[0]}'
        print(entities.EFFECTS_MENU.get(index_subset[i])[0])
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
