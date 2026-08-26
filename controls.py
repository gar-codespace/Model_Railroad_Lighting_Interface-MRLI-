import entities
import model
import view
import effects
import audio


class UserInterface():
    '''
    The user interface is everything on the front panel of the machine.
    '''

    def __init__(self):

        entities.DISPLAY_MODE = 'WELCOME'
        self.standby_toggle: str
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


################ methods in main - UASYNCIO.gather ##################


    def run_effect(self):
        '''
        A lighting effect is always being run.
        '''

        self.effect.set_up_effect()

        while True:

            if entities.WP_DUR <= 0:
                self.effect.set_next_waypoint()
            else:
                entities.RED -= entities.STEP_R
                entities.GREEN -= entities.STEP_G
                entities.BLUE -= entities.STEP_B
                entities.WARM -= entities.STEP_W
                entities.COOL -= entities.STEP_C
                self.effect.set_led_values()

            entities.WP_DUR -= 1
            if entities.DISPLAY_MODE == 'ANIMATED':
                self.update_display(view.get_status_screen())

            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

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
        Consolidate all the front panel led buttons into one loop.
        '''

        bC = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_callback)
        bB = entities.Button(entities.PICO_PIN['BACK'], True, self.back_button_callback)
        b0 = entities.Button(entities.PICO_PIN['BANK_0_B'], True, self.bank_button_callback, 'BANK_0')
        b1 = entities.Button(entities.PICO_PIN['BANK_1_B'], True, self.bank_button_callback, 'BANK_1')
        b2 = entities.Button(entities.PICO_PIN['BANK_2_B'], True, self.bank_button_callback, 'BANK_2')
        b3 = entities.Button(entities.PICO_PIN['BANK_3_B'], True, self.bank_button_callback, 'BANK_3')
        b4 = entities.Button(entities.PICO_PIN['BANK_4_B'], True, self.bank_button_callback, 'BANK_4')
        bs = entities.Button(entities.PICO_PIN['SCENIC_B'], True, self.bank_button_callback, 'SCENIC')

        while(True):

            bC.update()
            # bB.update()
            if entities.DISPLAY_MODE == 'STATIC' or entities.DISPLAY_MODE == 'EDIT':
                b0.update()
                b1.update()
                b2.update()
                b3.update()
                b4.update()
                bs.update() # that's an s not a 5

            await entities.UASYNCIO.sleep_ms(entities.DEFAULT_CYCLE)


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
            entities.DISPLAY_MODE = self.standby_toggle
            self.effect.set_led_banks()
            self.update_display(view.get_menu_list())

        else:
            self.standby_toggle = entities.DISPLAY_MODE
            entities.DISPLAY_MODE = 'STANDBY'
            self.effect.shut_off_leds()
            self.clear_display()


################# callbacks ##################


    def turn_left_callback(self):
        
        attrib = f'{entities.DISPLAY_MODE}_turn_left'

        try:
            display_content = getattr(view, attrib)() # IE view.WELCOME_turn_left()
            self.update_display(display_content)
        except:
            pass

        self.effect.set_led_values() # Real time color adjustment

    def turn_right_callback(self):
        attrib = f'{entities.DISPLAY_MODE}_turn_right'
        try:
            display_content = getattr(view, attrib)() # IE view.WELCOME_turn_right()
            self.update_display(display_content)
        except:
            pass

        self.effect.set_led_values()

    def single_click_callback(self):

        if entities.DISPLAY_MODE == 'EFFECTS':
            entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
            # print(entities.CURRENT_EFFECT)
            self.effect.set_up_effect()

        attrib = f'{entities.DISPLAY_MODE}_click'
        try:
            display_content = getattr(view, attrib)() # IE WELCOME_click()
            self.update_display(display_content)
        except:
            pass

    def multi_click_callback(self, clicks):
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

    def confirm_button_callback(self, name, event):
        '''Toggle standby mode.'''

        if event == entities.Button.RELEASED:
            self.toggle_standby()
            
    def back_button_callback(self, name, event):
        '''Not used.'''

        if event == entities.Button.RELEASED:
            print(name)

    def bank_button_callback(self, name, event):
        '''The LED bank and scenic buttons'''

        if event == entities.Button.RELEASED:
            index = entities.CURRENT_EFFECT[2]
            switch = f'{name}_S'

            entities.PIN(entities.PICO_PIN[switch]).toggle()
            entities.STATIC[name][index] = entities.PIN(entities.PICO_PIN[switch]).value()
