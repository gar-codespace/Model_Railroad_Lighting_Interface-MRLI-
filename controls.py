'''
I'm trying to keep this as vinella as possible
'''

import entities

# make a handler for each button
class ConfirmHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1 or entities.CURRENT_ROUTINE == 2:
            entities.PIN(entities.PICO_PIN['SCENIC']).toggle()

class BackHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")

class Bank0Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK0']).toggle()

class Bank1Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK1']).toggle()
            
class Bank2Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK2']).toggle()

class Display():

    # Generic code to create a specific display

    def __init__(self, list):

        self.bus = list[0]
        self.width = list[1]
        self.height = list[2]
        self.addr = list[3]

    def getDisplay(self):

        i2c = entities.I2C(
                        self.bus,
                        sda = entities.PIN(entities.PICO_PIN['SDA']),
                        scl = entities.PIN(entities.PICO_PIN['SCL']),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)


class DisplayModule():
    '''
    The display module is considered the display and encoder
    Integrates the rotary encoder and the display
    the confirm and back buttons are on my specific
    display are handled seperately
    '''

    def __init__(self):

        # rotary encoder pins
        self.push = entities.PICO_PIN['PSH']
        self.dt = entities.PICO_PIN['TRA']
        self.clk = entities.PICO_PIN['TRB']

        # Define the rotary encoder and the button
        self.encoder_pin_dt = entities.PIN(self.dt, entities.PIN.IN, entities.PIN.PULL_UP) # Try these w/o pull up
        self.encoder_pin_clk = entities.PIN(self.clk, entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_pin_sw = entities.PIN(self.push, entities.PIN.IN, entities.PIN.PULL_UP)

        # Define the display
        self.menu_display = entities.MENU_DISPLAY
        self.line_height = self.menu_display[4]
        self.menu_rows = self.menu_display[5]
        self.x_offset = self.menu_display[6]
        self.highlight_row = self.menu_display[7]
        self.display = Display(self.menu_display).getDisplay()

        # menu creation
        self.routines = entities.ROUTINES
        self.current_routine = entities.CURRENT_ROUTINE
        self.highlighted_item = entities.CURRENT_ROUTINE
        self.highlight = entities.MENU_HIGHLIGHT
        self.menu_top = 2 # move this into entities

    def display_splash(self):
        line_y = 0
        self.display.fill(0)
        for i in range(len(entities.SPLASH_SCREEN)):
            self.display.text(entities.SPLASH_SCREEN[i], self.x_offset, line_y)
            line_y += self.line_height
        self.display.show()

    def get_interface(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_pin_clk,
                                            pin_dt=self.encoder_pin_dt,
                                            pin_sw=self.encoder_pin_sw
                                            )

        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)

        # additional listeners
        # encoder.on(entities.RotaryEncoderEvent.ANY, self.any_event_listener)
        # encoder.on(entities.RotaryEncoderEvent.TURN_LEFT_FAST, self.turn_left_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT_FAST, self.turn_right_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.RELEASED, self.released_listener)
        # encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multy_click_listener)
        # encoder.on(entities.RotaryEncoderEvent.HELD, self.held_listener)

        return encoder

    def get_menu_items(self, direction):
        # direction is passed in as a boolean

        # format of sub_list is {0:7, 1:8, 2:0, 3:1, 4:2}
        sub_list = tuple(range(0, len(self.routines)))
        imenu_items_doubled = sub_list + sub_list

        sub_list = {}

        # print(direction)
        start = self.menu_top + 1
        if direction:
            start = self.menu_top - 1

        for i in range (self.menu_rows):
            sub_list[i] = imenu_items_doubled[start]
            start += 1

        # print(sub_list)
        self.menu_top = sub_list[0]

        return sub_list

    def get_menu(self, direction):

        line_y = 0
        menu_items = self.get_menu_items(direction)

        # self.display.rect(0, 24, 128, 15, 1) # eliminate hard coding
        highlight = entities.MENU_HIGHLIGHT
        self.display.rect(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4])

        for i in range (self.menu_rows):
            menu_item = self.routines[menu_items[i]]
            display_item = getattr(entities, menu_item, 'DAY')['name']
            self.display.text(display_item, self.x_offset, line_y)
            line_y += self.line_height

            self.highlighted_item = menu_items[self.highlight_row]

        return self.display

    # The left and right listeners are backwards for my display
    def turn_left_listener(self):
        self.display.fill(0)
        self.get_menu(False)
        self.display.show()

    def turn_right_listener(self):
        self.display.fill(0)
        self.get_menu(True)
        self.display.show()

    def single_click_listener(self):
        entities.CURRENT_ROUTINE = self.highlighted_item
        # print(f'Selected routine: ' + str(entities.CURRENT_ROUTINE))

    # These are not used
    # def any_event_listener(self, event, clicks):
    #     print(f"ANY Event ID: {event} Clicks: {clicks}")
# 
    # def turn_left_fast_listener(self):
    #     print(f"Turn Left Fast")
# 
    # def turn_right_fast_listener(self):
    #     print(f"Turn Right Fast")
    # 
    # def multy_click_listener(self, clicks):
    #     print(f"Multiply Clicks: {clicks}")
# 
    # def held_listener(self):
    #     print(f"Held")
# 
    # def released_listener(self):
    #     print(f"Released")

