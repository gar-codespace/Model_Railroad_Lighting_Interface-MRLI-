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

    line_y = 0
    for i in range(entities.MAIN_FORMAT['ROWS']):
        display.text(entities.WELCOME_SCREEN[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
        line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

    return

def status_screen(display):

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

    value = model.pwm2percent(entities.PWM_VALUES['WHITE'])
    display.text(f'White: {value}%', x, y)
    y += entities.MAIN_FORMAT['LINE_HEIGHT']

def status_hilight(display, direction: str):
    '''
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

def adjust_color_value(direction: str):

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

    







        # menu creation
        #self.routines = entities.ROUTINES
        #self.current_routine = entities.CURRENT_ROUTINE
        #self.highlighted_item = entities.CURRENT_ROUTINE
        #self.highlight = entities.MENU_HIGHLIGHT
        #self.menu_top = 2 # move this into entities



    # def get_menu_items(self, direction):
    #     # direction is passed in as a boolean
# 
    #     # format of sub_list is {0:7, 1:8, 2:0, 3:1, 4:2}
    #     sub_list = tuple(range(0, len(self.routines)))
    #     imenu_items_doubled = sub_list + sub_list
# 
    #     sub_list = {}
# 
    #     # print(direction)
    #     start = self.menu_top + 1
    #     if direction:
    #         start = self.menu_top - 1
# 
    #     for i in range (self.menu_rows):
    #         sub_list[i] = imenu_items_doubled[start]
    #         start += 1
# 
    #     # print(sub_list)
    #     self.menu_top = sub_list[0]
# 
    #     return sub_list
# 
    # def get_menu(self, direction):
# 
    #     line_y = 0
    #     menu_items = self.get_menu_items(direction)
# 
    #     # self.display.rect(0, 24, 128, 15, 1) # eliminate hard coding
    #     highlight = entities.MENU_HIGHLIGHT
    #     self.display.rect(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4])
# 
    #     for i in range (self.menu_rows):
    #         menu_item = self.routines[menu_items[i]]
    #         display_item = getattr(entities, menu_item, 'DAY')['name']
    #         self.display.text(display_item, self.x_offset, line_y)
    #         line_y += self.line_height
# 
    #         self.highlighted_item = menu_items[self.highlight_row]
# 
    #     return self.display