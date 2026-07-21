'''
I'm trying to keep this as simple as possible
The buttons on the display module are added here as they
will probably do something that affects the display.
The back button is roughed in but not implamented.
'''

import entities
import model
import view
import effects


class UserInterface():
    '''
    The control interface is the display, encoder, and additional
    buttons associated with the display module
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
        
        self.confirm = entities.Button(entities.PICO_PIN['CONFIRM'], True, self.confirm_button_listener)
        # self.back = entities.Button(entities.PICO_PIN['BACK'], True, self.back_button_listener)
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
            await entities.ASYNCIO.sleep_ms(entities.EFFECTS_TICK)

    def confirm_button_listener(self, button, event):
        if event == entities.Button.PRESSED:
            print(button)
        if event == entities.Button.RELEASED:
            print(button)

    def get_back(self): # not implemented

        while(True):
            self.back.update()
            await entities.ASYNCIO.sleep_ms(entities.EFFECTS_TICK)

    def back_button_listener(self, button, event): # not implemented
        pass

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
            entities.ASYNCIO.create_task(self.run_warm_effect())
            entities.ASYNCIO.create_task(self.run_cool_effect())

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

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('red effect finished')
        
    def run_green_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.GREEN_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('green effect finished')

    def run_blue_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.BLUE_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('blue effect finished')

    def run_warm_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.WARM_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('warm effect finished')

    def run_cool_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.COOL_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('cool effect finished')