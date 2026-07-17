'''
Creates and runs both the animated and non-animated routines.
'''

import entities

class Routine():

    def __init__(self):

        self.routine_parameters: dict = {}
        self.color_change_matrix: dict = {}
        self.red_pwm: int = 10000
        self.green_pwm: int = 10000
        self.blue_pwm: int = 10000
        self.warm_pwm: int = 10000
        self.white_pwm: int = 10000

        self.routine_ticks: int = 5000 # the length of the routine in ticks
        self.routine_midpoint_ticks: int = 2500

        self.switch0 = entities.PIN(entities.PICO_PIN['BANK0_S'])
        self.switch1 = entities.PIN(entities.PICO_PIN['BANK1_S'])
        self.switch2 = entities.PIN(entities.PICO_PIN['BANK2_S'])
        self.switch3 = entities.PIN(entities.PICO_PIN['BANK3_S'])
        self.switch4 = entities.PIN(entities.PICO_PIN['BANK4_S'])
        self.scenic= entities.PIN(entities.PICO_PIN['SCENIC_S'])

    def make_routine(self):
        print('make new routine')

    def increment_routine(self):
        pass

    # Coroutine: runs the selected routine
    def run_standin_routine(self):

        delay = entities.DEFAULT_TICK
        
        while True:            
            entities.LED.toggle()

            await entities.ASYNCIO.sleep_ms(delay)

    # Coroutine: runs the selected routine
    def run_routine(self):

        delay = entities.DEFAULT_TICK
        entities.SELECTED_ROUTINE = entities.CURRENT_ROUTINE
        self.make_routine()
        
        while True:

            if not entities.SELECTED_ROUTINE == entities.CURRENT_ROUTINE:
                entities.CURRENT_ROUTINE = entities.SELECTED_ROUTINE
                self.make_routine()

            self.increment_routine()
            entities.LED.toggle()

            await entities.ASYNCIO.sleep_ms(int(delay))
