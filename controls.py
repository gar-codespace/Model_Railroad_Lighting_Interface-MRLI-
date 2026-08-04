'''
I'm trying to keep this as simple as possible.
The Confirm button is used to turn the machine on or off.
When turning on it will start the last used effect from the beginning.
The Back button is not used.
'''

import entities
import model
import view
import audio
import effects
import listeners


class UserInterface():
    '''
    The user interface is everything on the front panel of the machine.
    '''

    def __init__(self):

        entities.SCREEN_MODE = 'AUTOMATIC'
        self.sound_card: object
        self.main_display: object

        model.set_switch_pins() # the switches that turn the led bank on or off
        
        self.effect = effects.Effect()
        self.effect.run_effect() # run entities.SELECTED_EFFECT

    def get_sound_card(self):

        self.sound_card = audio.get_sound_card(entities.SOUND_CARD)

    def get_main_display(self):

        self.main_display = view.get_display(entities.MAIN_DISPLAY)

    def show_welcome_screen(self):

        view.show_welcome_screen(self.main_display)

    def get_encoder(self):

        encoder_trb = entities.PIN(entities.PICO_PIN['TRB'], entities.PIN.IN, entities.PIN.PULL_UP)
        encoder_tra = entities.PIN(entities.PICO_PIN['TRA'], entities.PIN.IN, entities.PIN.PULL_UP)
        encoder_psh = entities.PIN(entities.PICO_PIN['PSH'], entities.PIN.IN, entities.PIN.PULL_UP)

        encoder = entities.RotaryEncoderRP2(pin_clk=encoder_trb,
                                            pin_dt=encoder_tra,
                                            pin_sw=encoder_psh
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
            self.effect.run_standby()
            view.show_blank_screen(self.main_display)
            entities.SCREEN_MODE = 'OFF'
        else:
            entities.SCREEN_MODE = 'AUTOMATIC'
            self.effect.run_effect()
            view.show_effects_screen(self.main_display)

        entities.MACHINE = not entities.MACHINE
        print(f'Machine State: {entities.MACHINE}')

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
            view.show_effects_screen(self.main_display)
        elif entities.SCREEN_MODE == 'MONITOR':
            pass
        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.main_display, 'left')
        elif entities.SCREEN_MODE == 'ADJUST':
            model.adjust_color_value('left')
            view.show_status_screen_manual(self.main_display, 'none')

    def turn_right_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_effect('right')
            view.show_effects_screen(self.main_display)
        elif entities.SCREEN_MODE == 'MONITOR':
            pass
        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.main_display, 'right')
        elif entities.SCREEN_MODE == 'ADJUST':
            model.adjust_color_value('right')
            view.show_status_screen_manual(self.main_display, 'none')

    def single_click_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC': # this is where effects get selected
            self.effect.run_effect()
            view.show_status_screen(self.main_display)
            entities.SCREEN_MODE = 'MONITOR'
        elif entities.SCREEN_MODE == 'MONITOR':
            model.reset_clocks()
            view.show_effects_screen(self.main_display)
            entities.SCREEN_MODE = 'AUTOMATIC'
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'ADJUST'
        elif entities.SCREEN_MODE == 'ADJUST':
            entities.SCREEN_MODE = 'MANUAL'
        print(f'Screen Mode: {entities.SCREEN_MODE}')

    def multi_click_listener(self, clicks):
        #print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_MODE == 'AUTOMATIC':
            entities.SCREEN_MODE = 'MANUAL'
            view.show_status_screen_manual(self.main_display, 'none')
        elif entities.SCREEN_MODE == 'MONITOR':
            entities.SCREEN_MODE = 'ADJUST'
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'AUTOMATIC'
            view.show_effects_screen(self.main_display)
        elif entities.SCREEN_MODE == 'ADJUST':
            pass

    def confirm_button_listener(self, button, event):
        '''Used to toggle the machine standby'''

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