'''
These are the methods that control the interface
'''

import entities


class Display1() :

    # Everything about the OLED display
    # Tuple items: buss, sda, scl, width, height, addr

    def __init__(self, list):

        self.result = ''
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


class Rotary():

    # Everything about the rotary encoder, including the buttons
    # dist items push, direction, step

    def __init__(self, rotary):

        self.result = ''
        self.push = rotary['push']
        self.dt = rotary['dt']
        self.clk = rotary['clk']

        # Define the pins for the rotary encoder and the button
        self.encoder_pin_dt = entities.PIN(self.dt, entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_pin_clk = entities.PIN(self.clk, entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_pin_sw = entities.PIN(self.push, entities.PIN.IN, entities.PIN.PULL_UP)

        self.display = Display1(entities.DISPLAY0).getDisplay()

    def getRotary(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_pin_clk, pin_dt=self.encoder_pin_dt, pin_sw=self.encoder_pin_sw)

        # subscribe to events
        # encoder.on(entities.RotaryEncoderEvent.ANY, self.any_event_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)

        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)

        # additional listeners
        # encoder.on(entities.RotaryEncoderEvent.TURN_LEFT_FAST, self.turn_left_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT_FAST, self.turn_right_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.RELEASED, self.released_listener)
        # encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multy_click_listener)
        # encoder.on(entities.RotaryEncoderEvent.HELD, self.held_listener)

        return encoder

    def any_event_listener(self, event, clicks):
        print(f"ANY Event ID: {event} Clicks: {clicks}")
    
    def turn_left_listener(self):
        self.display.fill(0)
        self.display.text(f"Turn Left", 0, 0)
        self.display.show()

    def turn_right_listener(self):
        self.display.fill(0)
        self.display.text(f"Turn Right", 0, 0)
        self.display.show()

    def turn_left_fast_listener(self):
        print(f"Turn Left Fast")

    def turn_right_fast_listener(self):
        print(f"Turn Right Fast")

    def single_click_listener(self):
        self.display.fill(0)
        self.display.text(f"Selected", 0, 0)
        self.display.show()
    
    def multy_click_listener(self, clicks):
        print(f"Multiply Clicks: {clicks}")

    def held_listener(self):
        print(f"Held")

    def released_listener(self):
        print(f"Released")
