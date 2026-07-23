'''
I'm trying to keep this as simple as possible
The buttons on the display module are added here as they
will probably do something that affects the display.
The back button is roughed in but not implemented.
'''

import entities
import model
import view
import effects


class UserInterface():
    '''
    The user interface is the display, encoder, and additional
    buttons associated with the display module
    '''

    def __init__(self):

        entities.SCREEN_MODE = 'AUTOMATIC'
        self.effect = effects.Effect()

        model.set_encoder_pins()
        model.set_switch_pins() # the switches that turn the led bank on or off
        # self.confirm = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_listener)
        # self.back = entities.Button(entities.PICO_PIN['BACK'], True, self.back_button_listener)
        
        self.display = view.Display(entities.MAIN_DISPLAY).getDisplay()

        view.show_welcome_screen(self.display)

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
    
    def get_confirm(self):
        ''' The confirm button on the display module'''

        while(True):
            self.confirm.update()
            await entities.ASYNCIO.sleep_ms(entities.EFFECTS_TICK)

    def confirm_button_listener(self, button, event):
        if event == entities.Button.PRESSED:
            print(button)
        if event == entities.Button.RELEASED:
            print(button)

    def get_back(self):
        ''' The back button on the display module'''

        while(True):
            self.back.update()
            await entities.ASYNCIO.sleep_ms(entities.EFFECTS_TICK)

    def back_button_listener(self, button, event):
        pass

    def turn_left_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_effect('left')
            view.show_effects_screen(self.display)
        elif entities.SCREEN_MODE == 'MONITOR':
            pass
        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.display, 'left')
        elif entities.SCREEN_MODE == 'ADJUST':
            model.adjust_color_value('left')
            view.show_status_screen_manual(self.display, 'none')

    def turn_right_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_effect('right')
            view.show_effects_screen(self.display)
        elif entities.SCREEN_MODE == 'MONITOR':
            pass
        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.display, 'right')
        elif entities.SCREEN_MODE == 'ADJUST':
            model.adjust_color_value('right')
            view.show_status_screen_manual(self.display, 'none')

    def single_click_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC': # this is where effects get selected
            entities.SCREEN_MODE = 'MONITOR'
            self.effect.run_effect()
            view.show_status_screen(self.display)
        elif entities.SCREEN_MODE == 'MONITOR':
            entities.SCREEN_MODE = 'AUTOMATIC'
            model.reset_clocks()
            view.show_effects_screen(self.display)
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'ADJUST'
        elif entities.SCREEN_MODE == 'ADJUST':
            entities.SCREEN_MODE = 'MANUAL'
            # update leds with new values here

    def multi_click_listener(self, clicks):
        #print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_MODE == 'AUTOMATIC':
            entities.SCREEN_MODE = 'MANUAL'
            view.show_status_screen_manual(self.display, 'none')
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'AUTOMATIC'
            view.show_effects_screen(self.display)
