import entities

def building_lights():
     # the lights that decorate the model buildings
    entities.PIN(entities.PICO_PIN['BANK5'], entities.PIN.OUT).value(0)


class Routine():

    def __init__(self):
        
        self.routine_parameters: dict = {}

        # Switch control, assigns each bank of lights to a Pico pin
        self.switch0 = entities.PIN(entities.PICO_PIN['BANK0'], entities.PIN.OUT)
        self.switch1 = entities.PIN(entities.PICO_PIN['BANK1'], entities.PIN.OUT)
        self.switch2 = entities.PIN(entities.PICO_PIN['BANK2'], entities.PIN.OUT)
        self.switch3 = entities.PIN(entities.PICO_PIN['BANK3'], entities.PIN.OUT)
        self.switch4 = entities.PIN(entities.PICO_PIN['BANK4'], entities.PIN.OUT)

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

    def get_routine_parameters(self):

        routine_index = entities.CURRENT_ROUTINE # int
        routine_name = entities.ROUTINES[routine_index] # string
        self.routine_parameters = getattr(entities, routine_name, 'DAY') # dict

    def set_light_banks(self, index):
        # turns each bank of lights on or off
        # for now each bank of lights stays on or off for the duration of the routine
        # format: 'bank0':(1, 1),
        self.switch0.value(self.routine_parameters['bank0'][index])
        self.switch1.value(self.routine_parameters['bank1'][index])
        self.switch2.value(self.routine_parameters['bank2'][index])
        self.switch3.value(self.routine_parameters['bank3'][index])
        self.switch4.value(self.routine_parameters['bank4'][index])

    def _get_pwm_value(self, setting=0):
        value = entities.PWM_STEPS * setting
        return int(value)
    
    def set_light_colors(self, index):
        # sets eachj lights brightness to its initial value
        # format: 'warm':(.8, .8, .8),
        
        self.red.duty_u16(self._get_pwm_value(self.routine_parameters['red'][index]))
        self.green.duty_u16(self._get_pwm_value(self.routine_parameters['green'][index]))
        self.blue.duty_u16(self._get_pwm_value(self.routine_parameters['blue'][index]))
        self.warm.duty_u16(self._get_pwm_value(self.routine_parameters['warm'][index]))
        self.white.duty_u16(self._get_pwm_value(self.routine_parameters['white'][index]))

    def make_new_routine(self):
        self.get_routine_parameters()
        self.set_light_banks(0)
        self.set_light_colors(0)

        # x = entities.RANDOM.randint(100, 700)

        return self.routine_parameters['test']
    
    def increment_routine(self):
        print('increment')

    # Coroutine: runs the selected routine
    def run_routine(self):
        delay_ms = 200
        run_this_routine = 0
        while True:
            # selected_routine = entities.CURRENT_ROUTINE
            if not run_this_routine == entities.CURRENT_ROUTINE:
                # create the routine here
                delay_ms = self.make_new_routine()
                print(f'Begin New Routine')
                run_this_routine = entities.CURRENT_ROUTINE
            entities.LED.toggle()
            self.increment_routine()
            # print(f'Current routine is: ' + str(run_routine))
            await entities.ASYNCIO.sleep_ms(delay_ms)

