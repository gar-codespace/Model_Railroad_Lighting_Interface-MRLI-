'''
I'm trying to keep this as simple as possible.
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

        effect_method = 'run_' + entities.DEFAULT_EFFECT[1] + '_effect'
        getattr(self.effect, effect_method)(entities.DEFAULT_EFFECT[2])

    def get_sound_card(self):

        self.sound_card = audio.get_sound_card()
        self.sound_card.volume = 22
        self.sound_card.volume_up()
        self.sound_card.volume_down()

    def play_default_sound(self):

        audio.play_default_sound(self.sound_card)

    def get_main_display(self):

        self.main_display = view.get_display(entities.MAIN_DISPLAY)

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

    def get_led_bank_buttons(self):
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
            if entities.DISPLAY_MODE == 'STATIC' or entities.DISPLAY_MODE == 'EDIT':
                b0.update()
                b1.update()
                b2.update()
                b3.update()
                b4.update()
                bs.update() # that's an s not a 5

            await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

    def update_display(self, content: list = entities.WELCOME_SCREEN):

        self.main_display.fill(0)

        line_y = 1
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.main_display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = entities.DISPLAY_MODE + '_get_hilight'
            h = getattr(view, attrib)()
            self.main_display.rect(0, h, 128, 12, 1)
        except:
            pass

        self.main_display.show()

    def clear_display(self):

        self.main_display.fill(0)
        self.main_display.show()

    def toggle_standby(self):

        if entities.DISPLAY_MODE == 'STANDBY':


            entities.DISPLAY_MODE = 'EFFECTS'
            effect_method = 'run_' + entities.CURRENT_EFFECT[1] + '_effect'
            getattr(self.effect, effect_method)(entities.CURRENT_EFFECT[2])
            display_content = view.get_menu_list()
            self.update_display(display_content)



        else:
            self.effect.run_STATIC_effect(0)
            self.clear_display()
            entities.DISPLAY_MODE = 'STANDBY'

    '''
    Display Modes:
    WELCOME - The initial greeting.
    EFFECTS - The menu of effects that are available.
    ANIMATED - Values for each color as the animated effect progresses.
    STATIC - Menu of color values available to edit.
    EDIT - One particular color is being edited.
    STANDBY - Static effect that turns everything 'off'.
    '''
    def turn_left_listener(self):
        attrib = entities.DISPLAY_MODE + '_turn_left'
        try:
            display_content = getattr(view, attrib)()
            self.update_display(display_content)
        except:
            pass

    def turn_right_listener(self):
        attrib = entities.DISPLAY_MODE + '_turn_right'
        try:
            display_content = getattr(view, attrib)()
            self.update_display(display_content)
        except:
            pass

    def single_click_listener(self):

        entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
        effect_method = 'run_' + entities.CURRENT_EFFECT[1] + '_effect'
        attrib = entities.DISPLAY_MODE + '_click'
        try:
            getattr(self.effect, effect_method)(entities.CURRENT_EFFECT[2])
            display_content = getattr(view, attrib)()
            self.update_display(display_content)
        except:
            pass

    def multi_click_listener(self, clicks):
        #print(f"Multiple Clicks: {clicks}")
        attrib = entities.DISPLAY_MODE + '_click2'
        try:
            display_content = getattr(view, attrib)()
            self.update_display(display_content)
        except:
            pass

    def confirm_button_listener(self, button, event):
        '''Used to toggle standby mode'''

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
