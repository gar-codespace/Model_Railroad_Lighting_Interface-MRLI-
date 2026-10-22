import entities
import states
import model
import view
import lighting
import sound


class Machine:
    '''
    The user interface initializes with the welcome screen displayed
    and a 'welcome' sound clip is played.
    '''

    def __init__(self):

# Initialize The Pico
    # The relays that turn the led banks on or off
        model.set_relay_pins()
    # Sets pico pins to pwm
        model.set_pwm_led_pins()
    # Front panel buttons use IRQ
        pin = entities.PIN(entities.PICO_PIN['CONFIRM'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_confirm_release, name='STANDBY')
        pin = entities.PIN(entities.PICO_PIN['BANK_0_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='BANK_0')
        pin = entities.PIN(entities.PICO_PIN['BANK_1_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='BANK_1')
        pin = entities.PIN(entities.PICO_PIN['BANK_2_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='BANK_2')
        pin = entities.PIN(entities.PICO_PIN['BANK_3_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='BANK_3')
        pin = entities.PIN(entities.PICO_PIN['BANK_4_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='BANK_4')
        pin = entities.PIN(entities.PICO_PIN['SCENIC_B'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        entities.IrqButton(params=entities.IRQ_BUTTON_0, pin=pin, cb_release=self.cb_bank_release, name='SCENIC')
    # Encoder uses polling
        self.encoder_tra = entities.PIN(entities.PICO_PIN['TRA'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.encoder_trb = entities.PIN(entities.PICO_PIN['TRB'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.encoder_psh = entities.PIN(entities.PICO_PIN['PSH'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
    # I2C
        self.sda = entities.PIN(entities.PICO_PIN['SDA'])
        self.scl = entities.PIN(entities.PICO_PIN['SCL'])
    # UART
        self.tx = entities.PIN(entities.PICO_PIN['TX'])
        self.rx = None
    #sound fx card
        self.reset = None
        # self.reset = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN) # Specific to the Adafruit SFX board

    def boot(self):
# Initialize The Machine
        self.main_display = view.Display(entities.OLED0, entities.I2C0)
        self.main_display.get_bus(pin0=self.sda, pin1=self.scl)
        self.main_display.get_display()

        self.sound = sound.Sound(entities.SB0, entities.UART0)
        self.sound.get_bus(pin0=self.tx, pin1=self.rx)
        self.sound.set_reset_pin(self.reset)
        self.sound.get_ambient_sound_board()
# Start The Machine
        entities.WORKING_BUFFER = entities.SINGLES
        model.get_menu_first_item()
        self.main_display.update_display(view.get_welcome_list())
        self.sound.play_sound() # Plays entities.CLIP, default is 'Welcome'
        lighting.fade_up_lights()

################ methods in main - UASYNCIO.gather ##################

    def run_lighting_effect(self): # How does this work without async?
        '''A lighting effect is always being run.'''

        while True:

            try: # set next waypoint
                view.put_progress_message()
                attrib = f'{entities.MACHINE_STATE}_set_next_waypoint'
                getattr(states, attrib)() # IE aniamated_set_next_waypoint()
            except:
                pass

            try: # only update colors when an animated effect is running
                attrib = f'{entities.MACHINE_STATE}_increment_waypoint'
                getattr(states, attrib)() # IE animated_increment_waypoint()
                lighting.set_pwm_values()
                self.main_display.update_display(view.get_status_list())
            except:
                pass

            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def play_ambient_effects(self): # How does this work without async?
        '''
        Ambient effects are designed to enhance the lighting effects.
        Ambient sound clips only play when the state is ANIMATED, STATIC, or EDIT.
        '''

        while True:

            sound.get_ambient_clip()
            duration = 1000

            try: # Play a sound clip
                attrib = f'{entities.MACHINE_STATE}_play_sound'
                getattr(states, attrib)() # IE states.animated_play_sound()
                duration = self.sound.play_sound_now()

                entities.PROGRESS_MESSAGE = f'Sound Clip: {entities.AMBIENCE[entities.CLIP][2]}'
                view.put_progress_message()

            except:
                pass

            try: # Run a visual effect if there is one
                attrib = f'{entities.MACHINE_STATE}_run_vfx'
                getattr(states, attrib)() # IE states.animated_run_vfx()
                lighting.run_vfx()
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

################# callbacks ##################

    def cb_turn_left(self):
        
        try:
            attrib = f'{entities.MACHINE_STATE}_turn_left'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_left()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_turn_right(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_turn_right'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_right()
            self.main_display.update_display(display_content)
        except:
            pass        

    def cb_single_click(self):

        try:
            attrib = f'{entities.MACHINE_STATE}_click'
            display_content = getattr(states, attrib)() # IE states.welcome_click()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_multi_click(self, clicks):
 
        try:
            attrib = f'{entities.MACHINE_STATE}_click2'
            display_content = getattr(states, attrib)() # IE states.welcome_click2()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_confirm_release(self, name, message):
        '''Toggle standby.'''

        try:
            attrib = f'{entities.MACHINE_STATE}_toggle' # IE states.standby_toggle()
            display_content = getattr(states, attrib)()
            self.main_display.update_display(display_content)
        except:
            pass

        self.sound.play_sound_now() # Plays the standby clips

    def cb_back_release(self, name, message):
        ...

    def cb_bank_release(self, name, message):
        '''The scenic and 5 LED bank buttons.'''

        index = entities.CURRENT_EFFECT[2]

        try:
            attrib = f'{entities.MACHINE_STATE}_bank' # IE states.edit_bank(name, index)
            getattr(states, attrib)(name, index)
        except:
            pass
