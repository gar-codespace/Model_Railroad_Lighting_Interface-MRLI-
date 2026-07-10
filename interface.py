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
                        sda = entities.PIN(self.sda),
                        scl = entities.PIN(self.scl),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)


class Controller():

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
        self.menu_top = 2 # move this into entities


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


class Button:
    """
    A simple Button class
    Create the button using Button(pinnumber, name, handler)
    handler is typically self, and create two methods buttonPressed and buttonReleased
    to handle the push and release of the button.
    The name of the button will be passed back to the handler to identify
    which button was pressed/released
    https://github.com/jitsengupta/PicoLibrary/blob/main/Button.py
    """
    
    def __init__(self, pin, name, *, handler=None, lowActive=True):
        """
        Initialize attributes and other internal data
        """
        
        self._pinNo = pin
        self._name = name
        if lowActive:
            self._pin = entities.PIN(pin, entities.PIN.IN, entities.PIN.PULL_UP)
        else:
            self._pin = entities.PIN(pin, entities.PIN.IN, entities.PIN.PULL_DOWN)
        self._debounce_time = 0
        self._lowActive = lowActive
        self._lastStatus = None
        self._handler = None
        self.setHandler(handler)
        
    def isPressed(self):
        """ Check if the button is pressed or not - useful if polling """
        
        status = (self._lowActive and self._pin.value() ==0) or (not self._lowActive and self._pin.value() == 1)
        return status
    
    def setHandler(self, handler):
        """ 
	    set the handler to a new handler. Pass None to remove existing handler
	    """
        
        # if the old handler was active already, or if the new handler is None, remove the irq
        if self._handler is not None or handler is None:
            self._pin.irq(handler = None)
    
        # Now set it to th enew handler
        self._handler = handler
        # Create the IRQ if the handler is not None
        if self._handler:
            self._pin.irq(trigger = entities.PIN.IRQ_FALLING | entities.PIN.IRQ_RISING, handler = self._callback)
        
    def _callback(self, pin):
        """ The private interrupt handler - will call appropriate handlers """
        
        t = entities.UTIME.ticks_ms()
        v = self._pin.value()
        if ((self._lastStatus == None or self._lastStatus != v) and t-self._debounce_time) > 50:
            self._debounce_time=t
            self._lastStatus = v
            if self._handler is not None:
                if self.isPressed():
                    self._handler.buttonPressed(self._name)
                else:
                    self._handler.buttonReleased(self._name)
        #self._debounce_time=t

# make a handler for each button
class ConfirmHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")

class BackHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")