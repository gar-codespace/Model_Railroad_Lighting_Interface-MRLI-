import entities

def building_lights():
     # the lights that decorate the model railroad
    entities.PIN(entities.PICO_PIN['SCENIC'], entities.PIN.OUT).value(0)


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

        # Switch control, assigns each bank of lights to a Pico pin
        self.switch0 = entities.PIN(entities.PICO_PIN['BANK0'], entities.PIN.OUT)
        self.switch1 = entities.PIN(entities.PICO_PIN['BANK1'], entities.PIN.OUT)
        self.switch2 = entities.PIN(entities.PICO_PIN['BANK2'], entities.PIN.OUT)
        self.scenic = entities.PIN(entities.PICO_PIN['SCENIC'], entities.PIN.OUT)

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
        self.scenic.value(self.routine_parameters['scenic'][index])

    def _get_pwm_value(self, setting=0):
        value = entities.PWM_STEPS * setting
        return int(value)
    
    def set_light_colors(self, index):
        # sets eachj lights brightness to its initial value
        # format: 'warm':(.8, .8, .8),
        x = self._get_pwm_value(self.routine_parameters['red'][index])
        self.red.duty_u16(int(x))
        self.red_pwm = x

        x = self._get_pwm_value(self.routine_parameters['green'][index])
        self.green.duty_u16(int(x))
        self.green_pwm = x

        x = self._get_pwm_value(self.routine_parameters['blue'][index])
        self.blue.duty_u16(int(x))
        self.blue_pwm = x

        x = self._get_pwm_value(self.routine_parameters['warm'][index])
        self.warm.duty_u16(int(x))
        self.warm_pwm = x

        x = self._get_pwm_value(self.routine_parameters['white'][index])
        self.white.duty_u16(int(x))
        self.white_pwm = x

    def _get_offset(self): # maybe put this in later

        offset = entities.ROUTINE_OFFSET * 60 # offset in seconds
        self.offset_ticks = int(offset / entities.ROUTINE_TICK)

    def _get_routine_duration(self):
        '''
        The duration is retrieved from the specs, it's in minutes.
        It's processed and returned as the number of ticks at the rate of entities.ROUTINE_TICK
        '''
        
        dur = self.routine_parameters['duration'] * 60 # the specified dur in seconds
        dur = dur / entities.CLOCK_RATIO # fast time in seconds
        dur = dur / 2 # chop the dur in half for the A and B parts of the routine
        rand_factor = 1 - self.routine_parameters['random'] # need it to be non-zero
        dur_minimum = dur * rand_factor
        duration_seconds = entities.RANDOM.randint(int(dur_minimum), int(dur)) # seconds
        self.routine_ticks = int(duration_seconds / entities.ROUTINE_TICK)

        self.routine_midpoint_ticks = int(self.routine_ticks / 2)

    def get_color_change_matrix(self):

        x = self._steps_per_tick(self.routine_parameters['red'][0], self.routine_parameters['red'][1])
        y = self._steps_per_tick(self.routine_parameters['red'][1], self.routine_parameters['red'][2])
        self.color_change_matrix['red'] = (int(x), int(y))

        x = self._steps_per_tick(self.routine_parameters['green'][0], self.routine_parameters['green'][1])
        y = self._steps_per_tick(self.routine_parameters['green'][1], self.routine_parameters['green'][2])
        self.color_change_matrix['green'] = (int(x), int(y))

        x = self._steps_per_tick(self.routine_parameters['blue'][0], self.routine_parameters['blue'][1])
        y = self._steps_per_tick(self.routine_parameters['blue'][1], self.routine_parameters['blue'][2])
        self.color_change_matrix['blue'] = (int(x), int(y))

        x = self._steps_per_tick(self.routine_parameters['warm'][0], self.routine_parameters['warm'][1])
        y = self._steps_per_tick(self.routine_parameters['warm'][1], self.routine_parameters['warm'][2])
        self.color_change_matrix['warm'] = (int(x), int(y))

        x = self._steps_per_tick(self.routine_parameters['white'][0], self.routine_parameters['white'][1])
        y = self._steps_per_tick(self.routine_parameters['white'][1], self.routine_parameters['white'][2])
        self.color_change_matrix['white'] = (int(x), int(y))

    def _steps_per_tick(self, begin, end):
        # how much does each color change per tick

        range  = begin - end
        scaler = entities.PWM_STEPS / self.routine_midpoint_ticks

        return int(range * scaler)

    def make_new_routine(self):
        delay = entities.DEFAULT_TICK
        self.get_routine_parameters()
        self.set_light_banks(0)
        self.set_light_colors(0)
        self.get_color_change_matrix()

        if not self.routine_parameters['duration'] == 0:
            self._get_routine_duration()
            delay = entities.ROUTINE_TICK

        return int(delay * 1000) # return delay in milliseconds
    
    def increment_routine(self):

        self.routine_ticks -= 1
        if self.routine_ticks >= self.routine_midpoint_ticks: # before the midpoint
            self.red_pwm = self.red_pwm - self.color_change_matrix['red'][0]
            self.red.duty_u16(int(self.red_pwm))

            self.green_pwm = self.green_pwm - self.color_change_matrix['green'][0]
            self.green.duty_u16(int(self.green_pwm))

            self.blue_pwm = self.blue_pwm - self.color_change_matrix['blue'][0]
            self.blue.duty_u16(int(self.blue_pwm))

            self.warm_pwm = self.warm_pwm - self.color_change_matrix['warm'][0]
            self.warm.duty_u16(int(self.warm_pwm))

            self.white_pwm = self.white_pwm - self.color_change_matrix['white'][0]
            self.white.duty_u16(int(self.white_pwm))

        else: # after the midpoint
            self.red_pwm = self.red_pwm - self.color_change_matrix['red'][1]
            self.red.duty_u16(int(self.red_pwm))

            self.green_pwm = self.green_pwm - self.color_change_matrix['green'][1]
            self.green.duty_u16(int(self.green_pwm))

            self.blue_pwm = self.blue_pwm - self.color_change_matrix['blue'][1]
            self.blue.duty_u16(int(self.blue_pwm))

            self.warm_pwm = self.warm_pwm - self.color_change_matrix['warm'][1]
            self.warm.duty_u16(int(self.warm_pwm))

            self.white_pwm = self.white_pwm - self.color_change_matrix['white'][1]
            self.white.duty_u16(int(self.white_pwm))

        if self.routine_ticks << 0 and self.routine_parameters['loop']:
            self.make_new_routine()


    ##############################################################
    # Coroutine: runs the selected routine
    def run_routine(self):
        delay_ms = 200
        run_this_routine = 0
        while True:

            if not run_this_routine == entities.CURRENT_ROUTINE: # create the routine here
                delay_ms = self.make_new_routine()
                print(f'Begin New Routine')
                run_this_routine = entities.CURRENT_ROUTINE
            if not self.routine_parameters['duration'] == 0:
                self.increment_routine()
            
            entities.LED.toggle()
            await entities.ASYNCIO.sleep_ms(delay_ms)

