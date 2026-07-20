'''
I'm trying to keep this as simple as possible
'''

import entities
import model
import view
import effects




class UserInterface():
    '''
    The control interface is the display, encoder, and all the buttons
    used to control the Pico
    '''

    def __init__(self):

        entities.SCREEN_MODE = 'AUTOMATIC'
        self.effect = effects.Effect()

        self.red_time_delay = 0
        self.green_time_delay = 0
        self.blue_time_delay = 0
        self.warm_time_delay = 0
        self.cool_time_delay = 0

        model.set_encoder_pins()
        model.set_switch_pins()
        model.set_button_pins()
        
        self.confirm = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_listener)
        self.display = view.Display(entities.MAIN_DISPLAY).getDisplay()

        view.show_welcome_screen(self.display)

    def get_encoder(self):

        encoder = entities.RotaryEncoderRP2(pin_clk=entities.PIN(entities.PICO_PIN['TRB']),
                                            pin_dt=entities.PIN(entities.PICO_PIN['TRA']),
                                            pin_sw=entities.PIN(entities.PICO_PIN['PSH'])
                                            )
        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)
        encoder.on(entities.RotaryEncoderEvent.MULTIPLE_CLICK, self.multi_click_listener)

        return encoder 
    
    def get_confirm(self):

        while(True):
            self.confirm.update()
            await entities.ASYNCIO.sleep_ms(25)

    def confirm_button_listener(self, button, event):
        if event == entities.Button.PRESSED:
            print('confirm button pressed')
        if event == entities.Button.RELEASED:
            print('confirm button released')

    def turn_left_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_effect('left')
            view.show_effects_screen(self.display)

        elif entities.SCREEN_MODE == 'MONITOR':
            pass

        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.display, 'left')

        elif entities.SCREEN_MODE == 'ADJUST':
            view.adjust_color_value('left')
            view.show_status_screen_manual(self.display, 'none')

    def turn_right_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC':
            model.increment_current_effect('right')
            view.show_effects_screen(self.display)
            
        elif entities.SCREEN_MODE == 'MONITOR':
            pass

        elif entities.SCREEN_MODE == 'MANUAL':
            view.show_status_screen_manual(self.display, 'right')
            
        elif entities.SCREEN_MODE == 'ADJUST':
            view.adjust_color_value('right')
            view.show_status_screen_manual(self.display, 'none')

    def single_click_listener(self):
        if entities.SCREEN_MODE == 'AUTOMATIC': # this is where effects get selected
            entities.SCREEN_MODE = 'MONITOR'
            self.effect.make_effect()
            view.show_status_screen(self.display)
            #entities.UTIME.sleep(2) # give the coroutines time to stop
            entities.ASYNCIO.create_task(self.run_red_effect())
            entities.ASYNCIO.create_task(self.run_green_effect())
            entities.ASYNCIO.create_task(self.run_blue_effect())

        elif entities.SCREEN_MODE == 'MONITOR':
            entities.SCREEN_MODE = 'AUTOMATIC'
            model.reset_clocks()
            view.show_effects_screen(self.display)

        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'ADJUST'

        elif entities.SCREEN_MODE == 'ADJUST':
            entities.SCREEN_MODE = 'MANUAL'
            # update leds with new values here

    def multi_click_listener(self, clicks):
        #print(f"Multiply Clicks: {clicks}")
        if entities.SCREEN_MODE == 'AUTOMATIC':
            entities.SCREEN_MODE = 'MANUAL'
            view.show_status_screen_manual(self.display, 'none')
            
        elif entities.SCREEN_MODE == 'MANUAL':
            entities.SCREEN_MODE = 'AUTOMATIC'
            view.show_effects_screen(self.display)

    # Color coroutine: runs the selected effect, one for each color
    def run_red_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.RED_CLOCK > 0:
            pass

            # entities.PWM_VALUES['RED'] = entities.RED_CLOCK
            # entities.RED_CLOCK -= 250
            # print(entities.RED_CLOCK)
# 
            # view.show_status_screen(self.display)

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('red effect finished')
        
    def run_green_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.GREEN_CLOCK > 0:
            pass

            # entities.GREEN_CLOCK -= 250
            # print(entities.GREEN_CLOCK)

            # view.show_status_screen(self.display)

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('green effect finished')

    def run_blue_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.BLUE_CLOCK > 0:
            pass

            # entities.BLUE_CLOCK -= 250
            # print(entities.BLUE_CLOCK)
# 
            # view.show_status_screen(self.display)

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('blue effect finished')




    # Coroutine: runs the selected effect
    def run_effect(self):

        #delay = entities.DEFAULT_TICK
        delay = entities.EFFECTS_TICK
        r = effects.Effect()
        
        while True:

            if not entities.SELECTED_EFFECTS == entities.CURRENT_EFFECTS:
                entities.CURRENT_EFFECTS = entities.SELECTED_EFFECTS
                r.make_effect()
#
            r.increment_effect()
            entities.LED.toggle()
            if entities.SCREEN_MODE == 'MONITOR':
                view.show_status_screen(self.display)

            await entities.ASYNCIO.sleep_ms(delay)

    # Coroutine: runs the selected effect
    def run_standin_effect(self):
        ''' For testing. '''
       
        delay = entities.DEFAULT_TICK
        
        while True:            
            entities.LED.toggle()

            await entities.ASYNCIO.sleep_ms(delay)