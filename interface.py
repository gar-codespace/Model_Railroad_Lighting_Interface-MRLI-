import entities
import model


class Display() :# abstract this to inherit from SSD1360_I2C

    # Everything about the OLED display
    # this display shows the menu items
    # Tuple items: buss, sda, scl, width, height, addr

    def __init__(self, list):

        self.bus = list[0]
        self.sda = list[1]
        self.scl = list[2]
        self.width = list[3]
        self.height = list[4]
        self.addr = list[5]

    def getDisplay(self):

        i2c = entities.I2C(
                        self.bus,
                        sda = entities.PIN(self.sda), # maybe add PIN.PULL_UP
                        scl = entities.PIN(self.scl),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)


class Controller():

    # Everything everything to build a controller
    # Integrates the rotary encoder and the display

    # dist items push, direction, step
    def __init__(self, rotary):

        # rotary encoder
        self.push = rotary['psh']
        self.dt = rotary['tra']
        self.clk = rotary['trb']

        # Define the rotary encoder and the button
        self.encoder_pin_dt = entities.PIN(self.dt, entities.PIN.IN, entities.PIN.PULL_UP) # Try these w/o pull up
        self.encoder_pin_clk = entities.PIN(self.clk, entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_pin_sw = entities.PIN(self.push, entities.PIN.IN, entities.PIN.PULL_UP)

        # Define the display
        self.menu_display = entities.MENU_DISPLAY
        self.line_height = self.menu_display[6]
        self.menu_rows = self.menu_display[7]
        self.x_offset = self.menu_display[8]
        self.highlight_row = self.menu_display[9]
        self.display = Display(self.menu_display).getDisplay()

        # menu creation
        self.routines = entities.ROUTINES
        self.current_routine = entities.CURRENT_ROUTINE
        self.highlighted_item = entities.CURRENT_ROUTINE
        self.highlight = entities.MENU_HIGHLIGHT
        self.menu_top = 2


    def get_interface(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_pin_clk, pin_dt=self.encoder_pin_dt, pin_sw=self.encoder_pin_sw)

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

        self.display.rect(0, 24, 128, 15, 1) # eliminate hard coding

        for i in range (self.menu_rows):
            menu_item = self.routines[menu_items[i]]
            display_item = getattr(entities, menu_item, 'DAY')['name']
            self.display.text(display_item, self.x_offset, line_y)
            line_y += self.line_height

            self.highlighted_item = menu_items[self.highlight_row]

        return self.display

    # The left and right listeners are backwards
    def turn_left_listener(self): # really the right turn listener
        self.display.fill(0)
        self.get_menu(False)
        self.display.show()

    def turn_right_listener(self):
        self.display.fill(0)
        self.get_menu(True)
        self.display.show()

    def single_click_listener(self):
        entities.CURRENT_ROUTINE = self.highlighted_item
        print(f'Selected routine: ' + str(entities.CURRENT_ROUTINE))
        # self.q.put(self.highlighted_item)
        # model.RunRoutine(self.highlighted_item).run()

    # These are not used
    def any_event_listener(self, event, clicks):
        print(f"ANY Event ID: {event} Clicks: {clicks}")

    def turn_left_fast_listener(self):
        print(f"Turn Left Fast")

    def turn_right_fast_listener(self):
        print(f"Turn Right Fast")
    
    def multy_click_listener(self, clicks):
        print(f"Multiply Clicks: {clicks}")

    def held_listener(self):
        print(f"Held")

    def released_listener(self):
        print(f"Released")
