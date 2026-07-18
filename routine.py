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

        routine_params = self._get_routine_parameters()
        
        if routine_params['duration'] == 0:
            self.make_static_routine(routine_params)

    def _get_routine_parameters(self):

        routine_name = entities.ROUTINES[entities.CURRENT_ROUTINE] # string, IE OFF or DAY
        
        return getattr(entities, routine_name, 'DAY') # dict

    def make_static_routine(self, routine_params):

        self.set_pwm_values(routine_params, 0)
        self.set_switch_status(routine_params, 0)
        self.set_led_values(routine_params)

    def set_pwm_values(self, routine_params, index=0):

        x = routine_params['red'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['RED'] = x
        x = routine_params['green'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['GREEN'] = x
        x = routine_params['blue'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['BLUE'] = x
        x = routine_params['warm'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['WARM'] = x
        x = routine_params['cool'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['COOL'] = x

    def set_switch_status(self, routine_params, index=0):

        entities.PIN(entities.PICO_PIN['BANK0_S']).value(routine_params['bank0'][index])
        entities.PIN(entities.PICO_PIN['BANK1_S']).value(routine_params['bank1'][index])
        entities.PIN(entities.PICO_PIN['BANK2_S']).value(routine_params['bank2'][index])
        entities.PIN(entities.PICO_PIN['BANK3_S']).value(routine_params['bank3'][index])
        entities.PIN(entities.PICO_PIN['BANK4_S']).value(routine_params['bank4'][index])
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(routine_params['scenic'][index])

    def set_led_values(self, routine_params):

        entities.PWM(entities.PIN(entities.PICO_PIN['RED'])).duty_u16(int(entities.PWM_VALUES['RED']))
        entities.PWM(entities.PIN(entities.PICO_PIN['GREEN'])).duty_u16(int(entities.PWM_VALUES['GREEN']))
        entities.PWM(entities.PIN(entities.PICO_PIN['BLUE'])).duty_u16(int(entities.PWM_VALUES['BLUE']))
        entities.PWM(entities.PIN(entities.PICO_PIN['WARM'])).duty_u16(int(entities.PWM_VALUES['WARM']))
        entities.PWM(entities.PIN(entities.PICO_PIN['COOL'])).duty_u16(int(entities.PWM_VALUES['COOL']))

    def increment_routine(self):
        pass
