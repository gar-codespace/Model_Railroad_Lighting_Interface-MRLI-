'''
Model Railroad Lighting Interface (MRLI)
'''

import entities
import states
import model
import view
import lighting
import sound


class MRLI:
    '''
    MRLI initializes with the welcome screen displayed
    and a 'welcome' sound clip is played.
    '''

    def __init__(self):

# Initialize The Pico
    # The relays that turn the led banks on or off
        model.set_relay_pins()
    # Sets pico pins to pwm
        model.set_pwm_led_pins()
    # Front panel buttons
        self.bC = model.get_button(pico_pin=entities.PICO_PIN['CONF_0_B'], params=entities.BUTTON_0, name='STANDBY')
        self.b0 = model.get_button(pico_pin=entities.PICO_PIN['BANK_0_B'], params=entities.BUTTON_0, name='BANK_0')
        self.b1 = model.get_button(pico_pin=entities.PICO_PIN['BANK_1_B'], params=entities.BUTTON_0, name='BANK_1')
        self.b2 = model.get_button(pico_pin=entities.PICO_PIN['BANK_2_B'], params=entities.BUTTON_0, name='BANK_2')
        self.b3 = model.get_button(pico_pin=entities.PICO_PIN['BANK_3_B'], params=entities.BUTTON_0, name='BANK_3')
        self.b4 = model.get_button(pico_pin=entities.PICO_PIN['BANK_4_B'], params=entities.BUTTON_0, name='BANK_4')
        self.bS = model.get_button(pico_pin=entities.PICO_PIN['SCENIC_B'], params=entities.BUTTON_0, name='SCENIC')

        self.bC.on(event=self.bC.RELEASE, callback=self.cb_conf_release)
        self.b0.on(event=self.b0.RELEASE, callback=self.cb_bank_release)
        self.b1.on(event=self.b1.RELEASE, callback=self.cb_bank_release)
        self.b2.on(event=self.b2.RELEASE, callback=self.cb_bank_release)
        self.b3.on(event=self.b3.RELEASE, callback=self.cb_bank_release)
        self.b4.on(event=self.b4.RELEASE, callback=self.cb_bank_release)
        self.bS.on(event=self.bS.RELEASE, callback=self.cb_bank_release)
    # Rotary Encoder
        self.en = model.get_encoder(pico_tra=entities.PICO_PIN['TRA'], pico_trb=entities.PICO_PIN['TRB'], pico_psh=entities.PICO_PIN['PSH'], params=entities.ENCODER_0)
        self.en.on(event=self.en.CW, callback=self.cb_clock_wise)
        self.en.on(event=self.en.ACW, callback=self.cb_anti_clock_wise)
        self.en.on(event=self.en.CLICK, callback=self.cb_click)
        self.en.on(event=self.en.MULTI, callback=self.cb_multi)

    def boot(self):
# Initialize the interface
        self.main_display = view.Display(entities.DISPLAY_0) # Big OLED
        # self.main_display = view.Display(entities.DISPLAY_1) # Small OLED
        self.sound = sound.Sound(entities.SOUND_CARD_0)
        model.logger()
# Start the interface
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
                attrib = f'{entities.MACHINE_STATE}_set_next_waypoint'
                getattr(states, attrib)() # IE states.aniamated_set_next_waypoint()
            except:
                pass

            try: # increment_waypoint only for animated effects
                attrib = f'{entities.MACHINE_STATE}_increment_waypoint'
                getattr(states, attrib)() # IE states.animated_increment_waypoint()
                lighting.set_pwm_values()
                self.main_display.update_display(view.get_status_list())
            except:
                pass

            model.logger()
            await entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE)

    def play_ambient_effects(self):
        '''
        Ambient effects are designed to enhance the lighting effects.
        Ambient sound clips only play when the state is ANIMATED, STATIC, or EDIT.
        '''

        while True:

            duration = 1000

            try: # Play a sound clip
                attrib = f'{entities.MACHINE_STATE}_play_sound'
                getattr(states, attrib)() # IE states.animated_play_sound(), used as a boolean
                sound.get_ambient_clip()
                duration = self.sound.play_sound()
                model.logger()
            except:
                pass

            try: # Run a visual effect
                attrib = f'{entities.MACHINE_STATE}_run_vfx'
                getattr(states, attrib)() # IE states.animated_run_vfx(), used as a boolean
                lighting.run_vfx()
                model.logger()
            except:
                pass

            wait = duration + sound.get_pad()
            await entities.UASYNCIO.sleep_ms(wait)            

    def poll_the_controls(self):

        while(True):

            self.en.poll()
            self.bC.poll()
            self.b0.poll()
            self.b1.poll()
            self.b2.poll()
            self.b3.poll()
            self.b4.poll()
            self.bS.poll() # that's an s not a 5

            await entities.UASYNCIO.sleep_ms(entities.DEFAULT_CYCLE)

################# callbacks ##################

    def cb_clock_wise(self, clicks):

        try:
            attrib = f'{entities.MACHINE_STATE}_turn_right'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_right()
            self.main_display.update_display(display_content)
        except:
            pass        

    def cb_anti_clock_wise(self, clicks):
        
        try:
            attrib = f'{entities.MACHINE_STATE}_turn_left'
            display_content = getattr(states, attrib)() # IE states.welcome_turn_left()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_click(self, clicks):

        try:
            attrib = f'{entities.MACHINE_STATE}_click'
            display_content = getattr(states, attrib)() # IE states.welcome_click()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_multi(self, clicks):
 
        try:
            attrib = f'{entities.MACHINE_STATE}_click2'
            display_content = getattr(states, attrib)() # IE states.welcome_click2()
            self.main_display.update_display(display_content)
        except:
            pass

    def cb_conf_release(self, name, message):
        '''The 'confirm' button on the display module, toggles standby.'''

        try:
            attrib = f'{entities.MACHINE_STATE}_toggle' # IE states.standby_toggle()
            display_content = getattr(states, attrib)()
            self.main_display.update_display(display_content)
        except:
            pass

        self.sound.play_sound_now() # Plays the standby clips

    def cb_back_release(self, name, message):
        '''The 'back' button on the display module.'''

    def cb_bank_release(self, name, message):
        '''The scenic and 5 LED bank buttons.'''

        index = entities.CURRENT_EFFECT[2]

        try:
            attrib = f'{entities.MACHINE_STATE}_bank' # IE states.edit_bank(name, index)
            getattr(states, attrib)(name, index)
        except:
            pass
