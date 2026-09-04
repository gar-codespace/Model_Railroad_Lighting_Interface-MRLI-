import entities
import states
import model
import view
import lighting
import audio


class UserInterface:
    '''
    The user interface is everything on the front panel of the machine.
    '''

    def __init__(self):

        self.main_display = view.get_display(entities.MAIN_DISPLAY)
        entities.MACHINE_STATE = 'WELCOME'
        self.standby_toggle: str
        self.sound_card: object

        model.set_switch_pins() # the switches that turn the led bank on or off
        model.set_pwm_led_pins() # sets pico pins to pwm

        self.effect = lighting.Effect()
        self.sfx = audio.SFX()


################ methods in main - UASYNCIO.gather ##################


    def run_lighting_effect(self):
        '''
        A lighting effect is always being run.
        '''

        self.effect.set_up_effect()
        entities.START_TIME = entities.UTIME.time()

        while True:

            if entities.WP_DUR <= 1:
                entities.END_TIME = entities.UTIME.time()
                print(f'Measured duration: {entities.END_TIME - entities.START_TIME} seconds')
                self.effect.set_next_waypoint()
                entities.START_TIME = entities.UTIME.time()

            try: # only update colors when an animated effect is running
                attrib = f'{entities.MACHINE_STATE}_increment_waypoint'
                getattr(model, attrib)() # IE ANIMATED_increment_waypoint()

                self.effect.set_led_values()
                self.update_display(view.get_status_list())
            except:
                pass

            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def run_sound_effects(self):
        '''
        Randomly picks a SFX from the SFX group.
        Adds a random ammount of time till the next SFX is played.
        '''

        while True:
            if not entities.MACHINE_STATE == 'STANDBY':

                self.sfx.get_sfx()
                # sfx_interval = entities.SFX_INTERVAL * 1000 # milliseconds
                # sfx_interval = entities.RANDINT(100, sfx_interval)
                # sfx_duration = entities.SFX_NAME[1] * 1000 # milliseconds

                self.sfx.unmute()
                self.sfx.play_sfx()

            else:
                self.sfx.mute()
                sfx_interval = 500
                sfx_duration = 500

            # await entities.UASYNCIO.sleep_ms(sfx_duration + sfx_interval)
            await entities.UASYNCIO.sleep_ms(40000)

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
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_callback)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_callback)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_callback)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multi_click_callback)

        return encoder 

    def get_all_the_buttons(self):
        '''
        Consolidate all the front panel buttons into one loop.
        '''

        bC = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_r_callback)
        # bB = entities.Button(entities.PICO_PIN['BACK'], True, self.back_button_r_callback)
        b0 = entities.Button(entities.PICO_PIN['BANK_0_B'], True, self.bank_button_r_callback, 'BANK_0')
        b1 = entities.Button(entities.PICO_PIN['BANK_1_B'], True, self.bank_button_r_callback, 'BANK_1')
        b2 = entities.Button(entities.PICO_PIN['BANK_2_B'], True, self.bank_button_r_callback, 'BANK_2')
        b3 = entities.Button(entities.PICO_PIN['BANK_3_B'], True, self.bank_button_r_callback, 'BANK_3')
        b4 = entities.Button(entities.PICO_PIN['BANK_4_B'], True, self.bank_button_r_callback, 'BANK_4')
        bS = entities.Button(entities.PICO_PIN['SCENIC_B'], True, self.bank_button_r_callback, 'SCENIC')

        while(True):

            bC.update()
            # bB.update()
            b0.update()
            b1.update()
            b2.update()
            b3.update()
            b4.update()
            bS.update() # that's an s not a 5

            await entities.UASYNCIO.sleep_ms(entities.DEFAULT_CYCLE)


################ display methods #################


    def update_display(self, content: list = entities.WELCOME_SCREEN):

        self.main_display.fill(0)

        line_y = 1
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.main_display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = f'{entities.MACHINE_STATE}_get_hilight'
            h = getattr(states, attrib)()
            self.main_display.rect(0, h, 128, 12, 1)
        except:
            pass

        self.main_display.contrast(entities.MAIN_DISPLAY_BRIGHTNESS)
        self.main_display.show()

    def clear_display(self):

        self.main_display.fill(0)
        self.main_display.show()


################# standby method ##################


    def toggle_standby(self):
        '''
        The effect is not stopped, the LEDs and SFX are turned off.
        '''

        if entities.MACHINE_STATE == 'STANDBY':
            entities.MACHINE_STATE = self.standby_toggle
            self.effect.set_led_banks()
            self.update_display(states.get_menu_list())
            # Turn on SFX

        else:
            self.standby_toggle = entities.MACHINE_STATE
            entities.MACHINE_STATE = 'STANDBY'
            self.effect.shut_off_leds()
            self.clear_display()
            # Turn off SFX


################# callbacks ##################


    def turn_left_callback(self):
        
        attrib = f'{entities.MACHINE_STATE}_turn_left'

        try:
            display_content = getattr(states, attrib)() # IE states.WELCOME_turn_left()
            self.update_display(display_content)
        except:
            pass

        self.effect.set_led_values() # Real time color adjustment

    def turn_right_callback(self):
        attrib = f'{entities.MACHINE_STATE}_turn_right'
        try:
            display_content = getattr(states, attrib)() # IE states.WELCOME_turn_right()
            self.update_display(display_content)
        except:
            pass

        self.effect.set_led_values()

    def single_click_callback(self):

        attrib = f'{entities.MACHINE_STATE}_select_sffect'
        try:
            getattr(self.effect, attrib)() # IE self.effect._select_sffect()
        except:
            pass

        attrib = f'{entities.MACHINE_STATE}_click'
        try:
            display_content = getattr(states, attrib)() # IE WELCOME_click()
            self.update_display(display_content)
        except:
            pass

    def multi_click_callback(self, clicks):
        #print(f"Multiple Clicks: {clicks}")
 
        attrib = f'{entities.MACHINE_STATE}_click2'
        try:
            display_content = getattr(states, attrib)() # IE WELCOME_click2()
            self.update_display(display_content)
        except:
            pass

    def confirm_button_r_callback(self, name, event):
        '''Toggle standby mode.'''

        self.toggle_standby()
            
    def back_button_r_callback(self, name, event):
        '''Not used.'''

        pass

    def bank_button_r_callback(self, name, event):
        '''The 6 LED bank and scenic buttons.'''

        index = entities.CURRENT_EFFECT[2]
        switch = f'{name}_S'

        entities.PIN(entities.PICO_PIN[switch]).toggle()
        entities.STATIC[name][index] = entities.PIN(entities.PICO_PIN[switch]).value()
