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
    # The relays that turn the led banks on or off
        model.set_relay_pins()
    # Sets pico pins to pwm
        model.set_pwm_led_pins()
    # Front panel buttons        
        pin = entities.PIN(entities.PICO_PIN['CONFIRM'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.bC = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_confirm_release, name='STANDBY')
        # pin = entities.PIN(entities.PICO_PIN['BACK'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        # self.bB = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_back_release, name=None)
        pin = entities.PIN(entities.PICO_PIN['BANK_0_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.b0 = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='BANK_0')
        pin = entities.PIN(entities.PICO_PIN['BANK_1_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.b1 = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='BANK_1')
        pin = entities.PIN(entities.PICO_PIN['BANK_2_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.b2 = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='BANK_2')
        pin = entities.PIN(entities.PICO_PIN['BANK_3_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.b3 = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='BANK_3')
        pin = entities.PIN(entities.PICO_PIN['BANK_4_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.b4 = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='BANK_4')
        pin = entities.PIN(entities.PICO_PIN['SCENIC_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.bS = entities.Button(params=entities.BUTTON0, pin=pin, cb_release=self.cb_bank_release, name='SCENIC')
    # Encoder
        self.encoder_trb = entities.PIN(entities.PICO_PIN['TRB'], entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_tra = entities.PIN(entities.PICO_PIN['TRA'], entities.PIN.IN, entities.PIN.PULL_UP)
        self.encoder_psh = entities.PIN(entities.PICO_PIN['PSH'], entities.PIN.IN, entities.PIN.PULL_UP)
    # I2C
        sda = entities.PIN(entities.PICO_PIN['SDA'])
        scl = entities.PIN(entities.PICO_PIN['SCL'])
    # UART
        tx = entities.PIN(entities.PICO_PIN['TX'])
        rx = None
        # reset_pin = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN) # Specific to the SFX board
# Initialize The Machine
        model.get_menu_first_item()
        entities.WORKING_BUFFER = entities.SINGLES
        self.standby_toggle: str

        i2c_bus = model.get_i2c(entities.I2C0, sda=sda, scl=scl)
        self.main_display = view.get_display(entities.MAIN_DISPLAY, i2c_bus)

        uart_bus = model.get_uart(entities.UART0, tx=tx, rx=rx)
        self.sound_fx_board = sound.get_sound_fx_board(entities.SB0, uart_bus)
# Start The Machine
        self.update_display(view.get_welcome_list())
        lighting.run_startup_effect()
        self.sound_fx_board.play(entities.WELCOME_CLIP)

################ methods in main - UASYNCIO.gather ##################

    def run_lighting_effect(self): # How does this work without async?
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

    def run_sound_effects(self): # How does this work without async?
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
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.cb_turn_left)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.cb_turn_right)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.cb_single_click)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.cb_multi_click)

        return encoder 

    def get_all_the_buttons(self): # How does this work without async?
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

            self.sound_fx_board.play_now(clip)

            print(f'Sound Clip: {clip} - {description}')

            return duration

################ visual effects method #################

    def run_vfx(self, sound_clip):
        '''Runs the associated visual effect if it exists.'''

        vfx = entities.SFX_LIBRARY[sound_clip][3]

        try:
            attrib = f'run_{vfx}'
            getattr(lighting, attrib)() # IE lighting.run_bolt()
        except:
            pass

################# callbacks ##################

    def cb_turn_left(self):
        
        try:
            attrib = f'{entities.MACHINE_STATE}_turn_left'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_left()
            self.update_display(display_content)
        except:
            pass

    def cb_turn_right(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_turn_right'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_right()
            self.update_display(display_content)
        except:
            pass        

    def cb_single_click(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_click'
            display_content = getattr(states, attrib)() # IE states.welcome_click()
            self.update_display(display_content)
        except:
            pass

    def cb_multi_click(self, clicks):
        #print(f"Multiple Clicks: {clicks}")
 
        try:
            attrib = f'{entities.MACHINE_STATE}_click2'
            display_content = getattr(states, attrib)() # IE states.welcome_click2()
            self.update_display(display_content)
        except:
            pass

    def cb_confirm_release(self, name, message):
        '''Toggle standby.'''

        try:
            attrib = f'{entities.MACHINE_STATE}_toggle' # IE states.standby_toggle()
            display_content = getattr(states, attrib)()
            self.update_display(display_content)
        except:
            pass

    def cb_back_release(self, name, message):
        '''Not used.'''

        pass

    def cb_bank_release(self, name, message):
        '''The scenic and 5 LED bank buttons.'''

        index = entities.CURRENT_EFFECT[2]

        try:
            attrib = f'{entities.MACHINE_STATE}_bank' # IE states.edit_bank(name, index)
            getattr(states, attrib)(name, index)
            print(f'{message}: {name}')
        except:
            pass
