'''
I'm trying to keep this as simple as possible
'''

import entities
import model
import view


class ControlInterface():
    '''
    The control interface is the display, encoder, and all the buttons
    used to control the Pico
    '''

    def __init__(self):

        model.set_encoder_pins()
        model.set_switch_pins()
        
        self.display = view.Display(entities.MAIN_DISPLAY).getDisplay()

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.display.fill(0)
        view.welcome_screen(self.display)
        self.display.show()

    def show_routines_screen(self):
        self.display.fill(0)

        self.display.show()

    def show_status_screen(self):
        self.display.fill(0)
        view.status_screen(self.display)
        self.display.show()

    def get_encoder(self):
        # Create the rotary encoder and selector object
        encoder = entities.RotaryEncoderRP2(pin_clk=entities.PIN(entities.PICO_PIN['TRB']),
                                            pin_dt=entities.PIN(entities.PICO_PIN['TRA']),
                                            pin_sw=entities.PIN(entities.PICO_PIN['PSH'])
                                            )

        # subscribe to events
        encoder.on(entities.RotaryEncoderEvent.TURN_LEFT, self.turn_left_listener)
        encoder.on(entities.RotaryEncoderEvent.TURN_RIGHT, self.turn_right_listener)
        encoder.on(entities.RotaryEncoderEvent.CLICK, self.single_click_listener)
        entities.Button(entities.PICO_PIN['CONFIRM'], "Return", handler=self.ReturnHandler())
        # entities.Button(entities.PICO_PIN['BACK'], "Back", handler=self.BackHandler())
        entities.Button(entities.PICO_PIN['BANK0_B'], "Bank0", handler=self.Bank0Handler())
        entities.Button(entities.PICO_PIN['BANK1_B'], "Bank1", handler=self.Bank1Handler())
        entities.Button(entities.PICO_PIN['BANK2_B'], "Bank2", handler=self.Bank2Handler())
        entities.Button(entities.PICO_PIN['SCENIC'], "Scenic", handler=self.ScenicHandler())

        return encoder
############################# ENCODER ##################################    
    def turn_left_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Left')

        elif entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'LEFT')
            self.display.show()

        elif entities.SCREEN_STATUS == 'ADJUST':
            view.adjust_color_value('LEFT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()

    def turn_right_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Right')

        elif entities.SCREEN_STATUS == 'STATUS':
            self.display.fill(0)
            view.status_screen(self.display)
            view.status_hilight(self.display, 'RIGHT')
            self.display.show()
            
        elif entities.SCREEN_STATUS == 'ADJUST':
            view.adjust_color_value('RIGHT')
            self.display.fill(0)
            view.status_screen(self.display)
            self.display.show()

    def single_click_listener(self):
        if entities.SCREEN_STATUS == 'ROUTINE':
            print('Select')

        elif entities.SCREEN_STATUS == 'STATUS':
            entities.SCREEN_STATUS = 'ADJUST'
            print(entities.SCREEN_STATUS)
            print(entities.STATUS_HILIGHT_INDEX)

        elif entities.SCREEN_STATUS == 'ADJUST':
            entities.SCREEN_STATUS = 'STATUS'
            print('Select')
            # update leds with new values
############################# BUTTONS ##################################
    class ReturnHandler:
        def buttonPressed(self, name):
            print(f"Handler: Button {name} pressed")
        def buttonReleased(self, name):
            print(f"Handler: Button {name} released")
            if entities.CURRENT_ROUTINE == 1 or entities.CURRENT_ROUTINE == 2:
                entities.PIN(entities.PICO_PIN['SCENIC']).toggle()
    # class BackHandler:
    #     def buttonPressed(self, name):
    #         print(f"Handler: Button {name} pressed")
    #     def buttonReleased(self, name):
    #         print(f"Handler: Button {name} released")
    class Bank0Handler:
        def buttonPressed(self, name):
            print(f"Handler: Button {name} pressed")
        def buttonReleased(self, name):
            print(f"Handler: Button {name} released")
            if entities.SCREEN_STATUS == 'STATUS':
                entities.PIN(entities.PICO_PIN['BANK0']).toggle()
    class Bank1Handler:
        def buttonPressed(self, name):
            print(f"Handler: Button {name} pressed")
        def buttonReleased(self, name):
            print(f"Handler: Button {name} released")
            if entities.SCREEN_STATUS == 'STATUS':
                entities.PIN(entities.PICO_PIN['BANK1']).toggle()
    class Bank2Handler:
        def buttonPressed(self, name):
            print(f"Handler: Button {name} pressed")
        def buttonReleased(self, name):
            print(f"Handler: Button {name} released")
            if entities.SCREEN_STATUS == 'STATUS':
                entities.PIN(entities.PICO_PIN['BANK2']).toggle()
    class ScenicHandler:
        def buttonPressed(self, name):
            print(f"Handler: Button {name} pressed")
        def buttonReleased(self, name):
            print(f"Handler: Button {name} released")
            if entities.SCREEN_STATUS == 'STATUS':
                entities.PIN(entities.PICO_PIN['SCENIC']).toggle()
