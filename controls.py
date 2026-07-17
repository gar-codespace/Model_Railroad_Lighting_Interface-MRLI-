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

        entities.SCREEN_MODE = 'AUTOMATIC'

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
        view.routine_screen(self.display)
        self.display.show()

    def show_status_screen(self):
        self.display.fill(0)
        view.status_screen(self.display)
        self.display.show()

    def get_encoder(self):

        encoder = entities.RotaryEncoderRP2(pin_clk=entities.PIN(entities.PICO_PIN['TRB']),
                                            pin_dt=entities.PIN(entities.PICO_PIN['TRA']),
                                            pin_sw=entities.PIN(entities.PICO_PIN['PSH'])
                                            )
        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multi_click_listener)

        return encoder 

    def turn_left_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_routine('left')
            self.show_routines_screen()

        elif entities.SCREEN_MODE == 'MONITOR':
            pass

        elif entities.SCREEN_MODE == 'MANUAL':
            self.display.fill(0)
            view.status_screen(self.display)
            view.manual_hilight(self.display, 'LEFT')
            self.display.show()

        elif entities.SCREEN_MODE == 'ADJUST':
            view.adjust_color_value('LEFT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()


    def turn_right_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_routine('right')
            self.show_routines_screen()

        elif entities.SCREEN_MODE == 'MONITOR':
            pass

        elif entities.SCREEN_MODE == 'MANUAL':
            self.display.fill(0)
            view.status_screen(self.display)
            view.manual_hilight(self.display, 'RIGHT')
            self.display.show()
            
        elif entities.SCREEN_MODE == 'ADJUST':
            view.adjust_color_value('RIGHT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()


    def single_click_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            print(entities.SELECTED_ROUTINE) # this is where routines get changed
            print(entities.SCROLL_ROUTINE)
            print(entities.CURRENT_ROUTINE)
            entities.CURRENT_ROUTINE = entities.SELECTED_ROUTINE
            entities.SCREEN_MODE = 'MONITOR'
            self.show_status_screen()

        elif entities.SCREEN_MODE == 'MONITOR':
            entities.SCREEN_MODE = 'AUTOMATIC'
            self.show_routines_screen()

        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'ADJUST'

        elif entities.SCREEN_MODE == 'ADJUST':
            entities.SCREEN_MODE = 'MANUAL'
            # update leds with new values


    def multi_click_listener(self, clicks):
        #print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_MODE == 'AUTOMATIC':
            entities.SCREEN_MODE = 'MANUAL'
            self.show_status_screen()
            
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'AUTOMATIC'
            self.show_routines_screen()
