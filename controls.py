'''
I'm trying to keep this as simple as possible.
The Confirm button is used to turn the machine on or off.
When turning on it will start the last used effect from the beginning.
The Back button is not used.
'''

import entities
import model
import view
# import audio
import effects
import listeners


class UserInterface():
    '''
    The user interface is everything on the front panel of the machine.
    '''

    def __init__(self):

        entities.SCREEN_MODE = 'AUTOMATIC'

        model.set_switch_pins() # the switches that turn the led bank on or off
        
        self.effect = effects.Effect()
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
    
    def get_confirm_button(self):
        ''' The confirm button on the display module'''
        self.confirm = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_listener)

        while(True):
            self.confirm.update()
            await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

    def get_back_button(self):
        ''' The back button on the display module'''
        self.back = entities.Button(entities.PICO_PIN['BACK'], True, listeners.back_button_listener)

        while(True):
            self.back.update()
            await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

    def toggle_machine_state(self):
        '''
        Use the confirm button to turn the machine off or on
        '''

        if entities.MACHINE:
            self.effect.shut_off()
            view.show_blank_screen(self.display)
            entities.SCREEN_MODE = 'OFF'
        else:
            entities.SCREEN_MODE = 'AUTOMATIC'
            self.effect.run_effect()
            view.show_effects_screen(self.display)

        entities.MACHINE = not entities.MACHINE
        print(entities.MACHINE)

    async def get_led_bank_buttons(self):
        '''
        Consolidate all the led buttons into one loop.
        ''' 

        b0 = entities.Button(entities.PICO_PIN['BANK0_B'], True, listeners.bank0_button_listener)
        b1 = entities.Button(entities.PICO_PIN['BANK1_B'], True, listeners.bank1_button_listener)
        b2 = entities.Button(entities.PICO_PIN['BANK2_B'], True, listeners.bank2_button_listener)
        b3 = entities.Button(entities.PICO_PIN['BANK3_B'], True, listeners.bank3_button_listener)
        b4 = entities.Button(entities.PICO_PIN['BANK4_B'], True, listeners.bank4_button_listener)
        bs = entities.Button(entities.PICO_PIN['SCENIC_B'], True, listeners.scenic_button_listener)

        while(True):
            if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
                b0.update()
                b1.update()
                b2.update()
                b3.update()
                b4.update()
                bs.update() # that's an s not a 5

            await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

    '''
    Screen Modes:
    AUTOMATIC - The display shows a menu of available lighting effects.
    MONITOR - The display shows the values of the 5 colors as the effect progresses.
    MANUAL - The display shows the menu of the 5 colors and their current value.
    ADJUST - The display shows the value of the selected color as it's being adjusted.
    OFF - The display is blank.
    '''
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
        # self.get_buttons()
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
        print(f'Screen Mode: {entities.SCREEN_MODE}')

    def multi_click_listener(self, clicks):
        #print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_MODE == 'AUTOMATIC':
            entities.SCREEN_MODE = 'MANUAL'
            view.show_status_screen_manual(self.display, 'none')
        elif entities.SCREEN_MODE == 'MONITOR':
            # add functionality to edit static routines
            entities.SCREEN_MODE = 'ADJUST'
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'AUTOMATIC'
            view.show_effects_screen(self.display)
        elif entities.SCREEN_MODE == 'ADJUST':
            pass

    def confirm_button_listener(self, button, event):
        '''Used to turn the machine on or off'''

        if event == entities.Button.PRESSED:
            pass
        if event == entities.Button.RELEASED:
            self.toggle_machine_state()

    def back_button_listener(self, button, event):
        '''Not used.'''

        if event == entities.Button.PRESSED:
            pass
        if event == entities.Button.RELEASED:
            print(button)