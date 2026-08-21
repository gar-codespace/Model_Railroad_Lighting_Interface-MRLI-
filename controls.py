'''
The Confirm button is used to toggle standby mode.
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

        entities.DISPLAY_MODE = 'WELCOME'
        self.sound_card: object
        self.main_display: object

        model.set_switch_pins() # the switches that turn the led bank on or off
        model.set_pwm_led_pins() # sets pico pins to pwm

        self.effect = effects.Effect()

    def run_default_effect(self):
        '''The default effect is entities.CURRENT_EFFECT'''

        self.effect.run_STATIC_effect()

    def get_sound_card(self):

        pass

    def play_default_sound(self):

        pass

    def get_main_display(self):

        self.main_display = view.get_display(entities.MAIN_DISPLAY)
        self.main_display.contrast(entities.MAIN_DISPLAY_BRIGHTNESS)


################ methods in main - ASYNCIO.gather ##################


    def clock_cycle_pulse(self):
        '''
        Sends out a signal to increment an animated effect.
        This runs even if the effect is static.
        '''

        while True:
            a = 1

            await entities.ASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def get_encoder(self):
        '''
        The await part is in async_tick.
        '''

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

    def get_led_bank_buttons(self):
        '''
        Consolidate all the led buttons into one loop.
        ''' 

        b0 = entities.Button(entities.PICO_PIN['BANK_0_B'], True, listeners.BANK_0_button_listener)
        b1 = entities.Button(entities.PICO_PIN['BANK_1_B'], True, listeners.BANK_1_button_listener)
        b2 = entities.Button(entities.PICO_PIN['BANK_2_B'], True, listeners.BANK_2_button_listener)
        b3 = entities.Button(entities.PICO_PIN['BANK_3_B'], True, listeners.BANK_3_button_listener)
        b4 = entities.Button(entities.PICO_PIN['BANK_4_B'], True, listeners.BANK_4_button_listener)
        bs = entities.Button(entities.PICO_PIN['SCENIC_B'], True, listeners.scenic_button_listener)

        while(True):
            if entities.DISPLAY_MODE == 'STATIC' or entities.DISPLAY_MODE == 'EDIT':
                b0.update()
                b1.update()
                b2.update()
                b3.update()
                b4.update()
                bs.update() # that's an s not a 5

            await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)


################ display methods #################


    def update_display(self, content: list = entities.WELCOME_SCREEN):

        self.main_display.fill(0)

        line_y = 1
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.main_display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = f'{entities.DISPLAY_MODE}_get_hilight'
            h = getattr(view, attrib)()
            self.main_display.rect(0, h, 128, 12, 1)
        except:
            pass

        self.main_display.show()

    def clear_display(self):

        self.main_display.fill(0)
        self.main_display.show()


################# standby method ##################


    def toggle_standby(self):
        '''
        The effect is not stopped, the LEDs are turned off.
        '''

        if entities.DISPLAY_MODE == 'STANDBY':
            entities.DISPLAY_MODE = 'EFFECTS'
            self.effect.set_led_banks()
            self.update_display(view.get_menu_list())

        else:
            entities.DISPLAY_MODE = 'STANDBY'
            self.effect.shut_off_leds()
            self.clear_display()


################# listeners ##################


    def turn_left_listener(self):
        attrib = f'{entities.DISPLAY_MODE}_turn_left'
        try:
            display_content = getattr(view, attrib)() # IE view.WELCOME_turn_left()
            self.update_display(display_content)
        except:
            pass

        self.effect._set_led_values() # Real time color adjustment

    def turn_right_listener(self):
        attrib = f'{entities.DISPLAY_MODE}_turn_right'
        try:
            display_content = getattr(view, attrib)() # IE view.WELCOME_turn_right()
            self.update_display(display_content)
        except:
            pass

        self.effect._set_led_values()

    def single_click_listener(self):

        entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)

        type = entities.CURRENT_EFFECT[1]
        if not type == 'STATIC':
            type = 'ANIMATED'
        effect_method = f'run_{type}_effect'

        try:
            getattr(self.effect, effect_method)()
        except:
            pass

        attrib = f'{entities.DISPLAY_MODE}_click'
        try:
            display_content = getattr(view, attrib)() # IE WELCOME_click()
            self.update_display(display_content)
        except:
            pass

    def multi_click_listener(self, clicks):
        #print(f"Multiple Clicks: {clicks}")
        update = f'{entities.DISPLAY_MODE}update_buffer' # IE view.EDITupdate_buffer()
        try:
            getattr(view, update)()
        except:
            pass
        attrib = f'{entities.DISPLAY_MODE}_click2'
        try:
            display_content = getattr(view, attrib)() # IE WELCOME_click2()
            self.update_display(display_content)
        except:
            pass

    def confirm_button_listener(self, button, event):
        '''Toggle standby mode.'''

        if event == entities.Button.PRESSED:
            pass
        if event == entities.Button.RELEASED:
            self.toggle_standby()
            
    def back_button_listener(self, button, event):
        '''Not used.'''

        if event == entities.Button.PRESSED:
            pass
        if event == entities.Button.RELEASED:
            print(button)
