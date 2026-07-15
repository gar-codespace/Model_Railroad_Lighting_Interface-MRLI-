'''
I'm trying to keep this as simple as possible
'''

import entities
import model
import view


class ControlInterface():
    '''
    The control interface is the display, encoder, and all the buttons
    used to control the Pico
    '''

    def __init__(self):

        model.set_encoder_pins()
        model.set_switch_pins()
        model.set_button_pins()
        
        self.display = view.Display(entities.MAIN_DISPLAY).getDisplay()

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.display.fill(0)
        view.welcome_screen(self.display)
        self.display.show()

    def show_routines_screen(self):
        self.display.fill(0)
        view.welcome_screen(self.display)
        self.display.show()

    def show_status_screen(self):
        self.display.fill(0)
        view.status_screen(self.display)
        self.display.show()

    def get_encoder(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=entities.PIN(entities.PICO_PIN['TRB']),
                                            pin_dt=entities.PIN(entities.PICO_PIN['TRA']),
                                            pin_sw=entities.PIN(entities.PICO_PIN['PSH'])
                                            )
        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multy_click_listener)

        return encoder 

    def turn_left_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Left')

        elif entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'LEFT')
            self.display.show()

        elif entities.SCREEN_STATUS == 'ADJUST':
            view.adjust_color_value('LEFT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()

    def turn_right_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Right')

        elif entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'RIGHT')
            self.display.show()
            
        elif entities.SCREEN_STATUS == 'ADJUST':
            view.adjust_color_value('RIGHT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()

    def single_click_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Select')

        elif entities.SCREEN_STATUS == 'STATUS':
            entities.SCREEN_STATUS = 'ADJUST'
            print(entities.SCREEN_STATUS)
            print(entities.STATUS_HILIGHT_INDEX)

        elif entities.SCREEN_STATUS == 'ADJUST':
            entities.SCREEN_STATUS = 'STATUS'
            print('Select')
            # update leds with new values

    def multy_click_listener(self, clicks):
        print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_STATUS == 'ROUTINE':
            entities.SCREEN_STATUS = 'STATUS'
            self.show_status_screen()
            
            
        elif entities.SCREEN_STATUS == 'STATUS':
            entities.SCREEN_STATUS = 'ROUTINE'
            self.show_welcome_screen()
            

        print(entities.SCREEN_STATUS)
