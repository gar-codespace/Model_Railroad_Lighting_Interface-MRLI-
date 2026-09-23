import entities
import states
import model
import view
import lighting
import sound


class UserInterface:
    '''The user interface initializes with the welcome screen displayed
    and entities.WELCOME_CLIP is played.
    '''

    def __init__(self):

    # Initialize The Pico
        model.set_relay_pins() # the relays that turn the led banks on or off
        model.set_pwm_led_pins() # sets pico pins to pwm
        self.bC = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_r_callback, 'STANDBY')
        # self.bB = entities.Button(entities.PICO_PIN['BACK'], True, self.back_button_r_callback)
        self.b0 = entities.Button(entities.PICO_PIN['BANK_0_B'], True, self.bank_button_r_callback, 'BANK_0')
        self.b1 = entities.Button(entities.PICO_PIN['BANK_1_B'], True, self.bank_button_r_callback, 'BANK_1')
        self.b2 = entities.Button(entities.PICO_PIN['BANK_2_B'], True, self.bank_button_r_callback, 'BANK_2')
        self.b3 = entities.Button(entities.PICO_PIN['BANK_3_B'], True, self.bank_button_r_callback, 'BANK_3')
        self.b4 = entities.Button(entities.PICO_PIN['BANK_4_B'], True, self.bank_button_r_callback, 'BANK_4')
        self.bS = entities.Button(entities.PICO_PIN['SCENIC_B'], True, self.bank_button_r_callback, 'SCENIC')
        self.encoder_trb = entities.PIN(entities.PICO_PIN['TRB'], entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_tra = entities.PIN(entities.PICO_PIN['TRA'], entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_psh = entities.PIN(entities.PICO_PIN['PSH'], entities.PIN.IN, entities.PIN.PULL_UP)
        sda = entities.PIN(entities.PICO_PIN['SDA'])
        scl = entities.PIN(entities.PICO_PIN['SCL'])
        tx = entities.PIN(entities.PICO_PIN['TX'])
        rx = None
        reset = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN) # Specific to the SFX board
    # Initialize The Machine
        model.get_menu_first_item()
        entities.WORKING_BUFFER = entities.SINGLES
        self.standby_toggle: str

        i2c_bus = model.get_i2c(entities.I2C0, sda=sda, scl=scl)
        self.main_display = view.get_display(entities.MAIN_DISPLAY, i2c_bus)

        uart_bus = model.get_uart(entities.UART0, tx=tx, rx=rx)
        self.main_sound_card = sound.get_sound_card(entities.MAIN_SOUND_CARD, uart_bus, reset_pin=reset)
    # Start The Machine
        self.update_display(view.get_welcome_list())
        self.main_sound_card.play_now(entities.WELCOME_CLIP)
    # Pick one, run time or testing.
        lighting.run_startup_effect() # This line is for run time
        #lighting.set_up_effect() # This line is for testing

################ methods in main - UASYNCIO.gather ##################

    def run_lighting_effect(self):
        '''A lighting effect is always being run.'''

        while True:

            try: # set next waypoint
                attrib = f'{entities.MACHINE_STATE}_set_next_waypoint'
                getattr(states, attrib)() # IE aniamated_set_next_waypoint()
            except:
                pass

            try: # only update colors when an animated effect is running
                attrib = f'{entities.MACHINE_STATE}_increment_waypoint'
                getattr(states, attrib)() # IE animated_increment_waypoint()

                lighting.set_led_values()
                self.update_display(view.get_status_list())
            except:
                pass

            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def run_sound_effects(self):
        '''Sound effect clips don't play when the state is WELCOME, PAUSED or STANDBY.'''

        while True:

            sound_clip = sound.get_sound_clip()
            duration = 1000

            try: # Play the sound clip
                attrib = f'{entities.MACHINE_STATE}_play_sound'
                getattr(states, attrib)() # IE states.animated_play_sound()
                duration = self.play_sound_clip(sound_clip) # TODO is there a better way?
            except:
                pass

            try: # Run a visual effect if there is one
                attrib = f'{entities.MACHINE_STATE}_run_vfx'
                getattr(states, attrib)() # IE states.animated_run_vfx()
                self.run_vfx(sound_clip)
            except:
                pass

            wait = duration + sound.get_pad()
            await entities.UASYNCIO.sleep_ms(wait)

    def get_encoder(self):
        '''The await part is in async_tick.'''

        encoder = entities.RotaryEncoderRP2(pin_clk=self.encoder_trb,
                                            pin_dt=self.encoder_tra,
                                            pin_sw=self.encoder_psh
                                            )
        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_callback)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_callback)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_callback)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multi_click_callback)

        return encoder 

    def get_all_the_buttons(self):
        '''Consolidate all the front panel buttons into one loop.'''

        while(True):

            self.bC.update()
            # self.bB.update()
            self.b0.update()
            self.b1.update()
            self.b2.update()
            self.b3.update()
            self.b4.update()
            self.bS.update() # that's an s not a 5

            await entities.UASYNCIO.sleep_ms(entities.DEFAULT_CYCLE)

################ display method #################

    def update_display(self, content: list = entities.WELCOME_SCREEN):
        '''One method to rule them all...'''

        self.main_display.fill(0)

        line_y = 3 # vertically center the text in the display
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

################ sound method #################

    def play_sound_clip(self, sound_clip):

            clip = entities.SFX_LIBRARY[sound_clip][0]
            duration = entities.SFX_LIBRARY[sound_clip][1] * 1000 # ms
            description = entities.SFX_LIBRARY[sound_clip][2]

            self.main_sound_card.play_now(clip)

            print(f'Sound Clip: {clip} - {description}')

            return duration

################ visual effects method #################

    def run_vfx(self, sound_clip):
        '''Runs the associated visual effect if it exists.'''

        vfx = entities.SFX_LIBRARY[sound_clip][3]

        if vfx:
            attrib = f'run_{vfx}'
            getattr(lighting, attrib)() # IE lighting.run_bolt()

################# callbacks ##################

    def turn_left_callback(self):
        
        try:
            attrib = f'{entities.MACHINE_STATE}_turn_left'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_left()
            self.update_display(display_content)
        except:
            pass

    def turn_right_callback(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_turn_right'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_right()
            self.update_display(display_content)
        except:
            pass        

    def single_click_callback(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_click'
            display_content = getattr(states, attrib)() # IE states.welcome_click()
            self.update_display(display_content)
        except:
            pass

    def multi_click_callback(self, clicks):
        #print(f"Multiple Clicks: {clicks}")
 
        try:
            attrib = f'{entities.MACHINE_STATE}_click2'
            display_content = getattr(states, attrib)() # IE states.welcome_click2()
            self.update_display(display_content)
        except:
            pass

    def confirm_button_r_callback(self, name, event):
        '''Toggle standby.'''

        try:
            attrib = f'{entities.MACHINE_STATE}_toggle' # IE states.standby_toggle()
            display_content = getattr(states, attrib)()
            self.update_display(display_content)
        except:
            pass

    def back_button_r_callback(self, name, event):
        '''Not used.'''

        pass

    def bank_button_r_callback(self, name, event):
        '''The 5 LED bank and scenic buttons.'''

        index = entities.CURRENT_EFFECT[2]

        try:
            attrib = f'{entities.MACHINE_STATE}_bank' # IE states.edit_bank(name, index)
            getattr(states, attrib)(name, index)
        except:
            pass
