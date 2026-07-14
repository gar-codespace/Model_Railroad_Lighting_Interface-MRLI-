'''
I'm trying to keep this as vinella as possible
'''

import entities
import listeners


class Display:
    '''
    Generic OLED display object
    '''

    def __init__(self, display_parameters):

        self.bus = display_parameters[0]
        self.width = display_parameters[1]
        self.height = display_parameters[2]
        self.addr = display_parameters[3]

    def get_display(self):

        i2c = entities.I2C(
                        self.bus,
                        sda = entities.PIN(entities.PICO_PIN['SDA']),
                        scl = entities.PIN(entities.PICO_PIN['SCL']),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)


class Encoder():

    def __init__(self):

        # rotary encoder pins
        self.push = entities.PICO_PIN['PSH']
        self.dt = entities.PICO_PIN['TRA']
        self.clk = entities.PICO_PIN['TRB']

        # Define the rotary encoder and the button
        self.encoder_pin_dt = entities.PIN(self.dt, entities.PIN.IN, entities.PIN.PULL_UP) # Try these w/o pull up
        self.encoder_pin_clk = entities.PIN(self.clk, entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_pin_sw = entities.PIN(self.push, entities.PIN.IN, entities.PIN.PULL_UP)

    def get_interface(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_pin_clk,
                                            pin_dt=self.encoder_pin_dt,
                                            pin_sw=self.encoder_pin_sw
                                            )

        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, listeners.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, listeners.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, listeners.single_click_listener)

        # additional listeners
        # encoder.on(entities.RotaryEncoderEvent.ANY, self.any_event_listener)
        # encoder.on(entities.RotaryEncoderEvent.TURN_LEFT_FAST, self.turn_left_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT_FAST, self.turn_right_fast_listener)
        # encoder.on(entities.RotaryEncoderEvent.RELEASED, self.released_listener)
        # encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multy_click_listener)
        # encoder.on(entities.RotaryEncoderEvent.HELD, self.held_listener)

        return encoder
