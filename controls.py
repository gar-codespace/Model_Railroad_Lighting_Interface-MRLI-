'''
I'm trying to keep this as vinella as possible
'''

import entities
import model
import view


class DisplayModule():
    '''
    The display module is the display and encoder, they work together.
    The confirm and back buttons are handled seperately.
    The left and right listeners are flipped for my display module.
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
        self.display = view.Display(entities.MAIN_DISPLAY).getDisplay()

    def show_welcome_screen(self):
        self.display.fill(0)
        view.welcome_screen(self.display)
        self.display.show()

    def show_routines_screen(self):
        self.display.fill(0)

        self.display.show()

    def show_status_screen(self):
        self.display.fill(0)
        view.status_screen(self.display)
        self.display.show()

    def get_encoder(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_pin_clk,
                                            pin_dt=self.encoder_pin_dt,
                                            pin_sw=self.encoder_pin_sw
                                            )

        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)

        return encoder

    def turn_left_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Left')

        if entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'LEFT')
            self.display.show()

        if entities.SCREEN_STATUS == 'ADJUST':
            print('Left')

    def turn_right_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Right')

        if entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'RIGHT')
            self.display.show()
            
        if entities.SCREEN_STATUS == 'ADJUST':
            print('Right')

    def single_click_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Select')

        if entities.SCREEN_STATUS == 'STATUS':
            print(entities.STATUS_HILIGHT_INDEX)

        if entities.SCREEN_STATUS == 'ADJUST':
            print('Select')


