'''
this is the class that makes and runs any routine
'''

import entities


class Routine():

    def __init__(self):
        # entities.CURRENT_ROUTINE is an integer, the key of the ROUTINES dictionary
        self.routine_parameters: dict = {}

        # Switch control, matches each bank of lights with a Pico pin
        self.p_switches = entities.P_SWITCHES
        self.switch0 = entities.PIN(self.p_switches[0], entities.PIN.OUT)
        self.switch1 = entities.PIN(self.p_switches[1], entities.PIN.OUT)
        self.switch2 = entities.PIN(self.p_switches[2], entities.PIN.OUT)
        self.switch3 = entities.PIN(self.p_switches[3], entities.PIN.OUT)
        self.switch4 = entities.PIN(self.p_switches[4], entities.PIN.OUT)
        self.switch5 = entities.PIN(self.p_switches[5], entities.PIN.OUT) # the lights in the model buildings

        # LED control, sets the Pico pins for PWM
        self.p_leds = entities.P_LEDS

        pwm = PWM(Pin(pin_number))
        self.red = entities.PWM(entities.PIN(self.p_leds['red']))

        
        self.red = entities.PIN(self.p_leds['red'])
        self.green = entities.PIN(self.p_leds['green'])
        self.blue = entities.PIN(self.p_leds['blue'])
        self.warm = entities.PIN(self.p_leds['warm'])
        self.white = entities.PIN(self.p_leds['white'])

    def make_new_routine(self):
        routine_index = entities.CURRENT_ROUTINE
        routine_name = entities.ROUTINES[routine_index] # string
        self.routine_parameters = getattr(entities, routine_name, 'DAY')
        self.set_light_banks()



    def set_light_banks(self):
        # turns each bank of lights on or off
        # for now each bank of lights stays on or off for the duration of the routine
        # format: 'bank0':(1, 1),
        self.switch0.value(self.routine_parameters['bank0'][0])
        self.switch1.value(self.routine_parameters['bank1'][0])
        self.switch2.value(self.routine_parameters['bank2'][0])
        self.switch3.value(self.routine_parameters['bank3'][0])
        self.switch4.value(self.routine_parameters['bank4'][0])
        self.switch5.value(self.routine_parameters['bank5'][0])




    # Coroutine: runs the selected routine
    def run_routine(self):
        delay_ms = 280
        run_routine = 0
        while True:
            selected_routine = entities.CURRENT_ROUTINE
            if not run_routine == selected_routine:
                # create the routine here
                self.make_new_routine()
                print('New Routine')
                run_routine = selected_routine
                #RunRoutine(run_routine).run()
            entities.LED.toggle()
            print(f'Current routine is: ' + str(run_routine))
            await entities.ASYNCIO.sleep_ms(delay_ms)

