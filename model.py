import entities


class Routine():

    def __init__(self):
        
        routine_index = entities.CURRENT_ROUTINE # int
        routine_name = entities.ROUTINES[routine_index] # string
        self.routine_parameters = getattr(entities, routine_name, 'DAY') # dict

        # Switch control, assigns each bank of lights to a Pico pin
        self.switch0 = entities.PIN(entities.PICO_PIN['BANK0'], entities.PIN.OUT)
        self.switch1 = entities.PIN(entities.PICO_PIN['BANK1'], entities.PIN.OUT)
        self.switch2 = entities.PIN(entities.PICO_PIN['BANK2'], entities.PIN.OUT)
        self.switch3 = entities.PIN(entities.PICO_PIN['BANK3'], entities.PIN.OUT)
        self.switch4 = entities.PIN(entities.PICO_PIN['BANK4'], entities.PIN.OUT)
        self.switch5 = entities.PIN(entities.PICO_PIN['BANK0'], entities.PIN.OUT) # the lights in the model buildings

        # LED control, sets the Pico pins for PWM
        self.red = entities.PWM(entities.PIN(entities.PICO_PIN['RED']))
        self.red.freq(entities.PWM_FREQ)
        self.green = entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']))
        self.green.freq(entities.PWM_FREQ)
        self.blue = entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']))
        self.blue.freq(entities.PWM_FREQ)
        self.warm = entities.PWM(entities.PIN(entities.PICO_PIN['WARM']))
        self.warm.freq(entities.PWM_FREQ)
        self.white = entities.PWM(entities.PICO_PIN['WHITE'])
        self.white.freq(entities.PWM_FREQ)

    def set_light_banks(self):
        # turns each bank of lights on or off
        # for now each bank of lights stays on or off for the duration of the routine
        # format: 'bank0':(1, 1),
        self.switch0.value(self.routine_parameters['bank0'][0])
        self.switch1.value(self.routine_parameters['bank1'][0])
        self.switch2.value(self.routine_parameters['bank2'][0])
        self.switch3.value(self.routine_parameters['bank3'][0])
        self.switch4.value(self.routine_parameters['bank4'][0])
        self.switch5.value(self.routine_parameters['bank5'][0]) # the lights in the model buildings

    def make_new_routine(self):
        self.set_light_banks()

    # Coroutine: runs the selected routine
    def run_routine(self):
        delay_ms = 280
        run_routine = 0
        while True:
            selected_routine = entities.CURRENT_ROUTINE
            if not run_routine == selected_routine:
                # create the routine here
                self.make_new_routine()
                print('Begin New Routine')
                run_routine = selected_routine
                #RunRoutine(run_routine).run()
            entities.LED.toggle()
            print(f'Current routine is: ' + str(run_routine))
            await entities.ASYNCIO.sleep_ms(delay_ms)

