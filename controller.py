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
    # Front panel buttons use polling
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
    # Encoder uses polling
        tra = entities.PIN(entities.PICO_PIN['TRA'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        trb = entities.PIN(entities.PICO_PIN['TRB'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        psh = entities.PIN(entities.PICO_PIN['PSH'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
        self.encoder = entities.RotaryEncoderRP2(pin_clk=trb, pin_dt=tra, pin_sw=psh)
        self.encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.cb_turn_left)
        self.encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.cb_turn_right)
        self.encoder.on(entities.RotaryEncoderEvent.CLICK, self.cb_single_click)
        self.encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.cb_multi_click)

    def boot(self):
# Initialize The Machine
        self.main_display = view.Display(entities.MAIN_DISPLAY0) # Big OLED
        # self.main_display = view.Display(entities.MAIN_DISPLAY1) # Small OLED
        self.main_display.get_bus()
        self.main_display.get_display()

        self.sound = sound.Sound(entities.SOUND_CARD0)
        self.sound.get_bus()
        self.sound.get_sound_board()
# Start The Machine
        entities.WORKING_BUFFER = entities.SINGLES
        model.get_menu_first_item()
        self.main_display.update_display(view.get_welcome_list())
        self.sound.play_sound() # Plays entities.CLIP, default is 'Welcome'
        lighting.fade_up_lights()

################ methods in main - await entities.UASYNCIO.gather ##################
# How do these work without using async def ...?

    def run_lighting_effect(self):

        while True:

            try: # set next waypoint only for animated effects
                view.put_progress_message()
                attrib = f'{entities.MACHINE_STATE}_set_next_waypoint'
                getattr(states, attrib)() # IE aniamated_set_next_waypoint()
            except:
                pass

            try: # increment_waypoint only for animated effects
                attrib = f'{entities.MACHINE_STATE}_increment_waypoint'
                getattr(states, attrib)() # IE states.animated_increment_waypoint()
                lighting.set_pwm_values()
                self.main_display.update_display(view.get_status_list())
            except:
                pass

            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def play_ambient_effects(self):
        '''
        Ambient effects are designed to enhance the lighting effects.
        Ambient sound clips only play when the state is ANIMATED, STATIC, or EDIT.
        '''

        while True:

            sound.get_ambient_clip()
            duration = 1000

            try: # Play an ambient sound clip
                attrib = f'{entities.MACHINE_STATE}_play_sound'
                getattr(states, attrib)() # IE states.animated_play_sound(), used as a boolean
                duration = self.sound.play_sound()

                entities.PROGRESS_MESSAGE = f'Sound Clip: {entities.AMBIENCE[entities.CLIP][2]}'
                view.put_progress_message()

            except:
                pass

            try: # Run an ambient visual effect
                attrib = f'{entities.MACHINE_STATE}_run_vfx'
                getattr(states, attrib)() # IE states.animated_run_vfx(), used as a boolean
                lighting.run_vfx()
            except:
                pass

            wait = duration + sound.get_pad()
            await entities.UASYNCIO.sleep_ms(wait)

    def poll_encoder(self):
        '''The await loop is in async_tick.'''

        return self.encoder 

    def poll_the_buttons(self):

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
