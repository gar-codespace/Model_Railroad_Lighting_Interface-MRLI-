'''
Creates and runs both the animated and non-animated effects.
'''

import entities

class Effect():

    def __init__(self):

        self.effect_parameters: dict = {}
        self.color_change_matrix: dict = {}
        self.red_pwm: int = 10000
        self.green_pwm: int = 10000
        self.blue_pwm: int = 10000
        self.warm_pwm: int = 10000
        self.white_pwm: int = 10000

        self.duration_ticks: int = 100# the length of the effect in ticks
        self.duration_midpoint: int = 50
        self.current_tick: int = 0
        self.loop: bool = True
        self.animation_matrix: dict = {}

    def make_effect(self):        

        effect_params = self._get_effect_parameters()
        self.current_tick = 0
        
        if effect_params['duration'] == 0:
            self.make_static_effect(effect_params)
            print('Static Effect')
        elif not effect_params['duration'] == 0:
            self.make_animated_effect(effect_params)
            print('Animated Effect')

    def _get_effect_parameters(self):

        effect_name = entities.EFFECTSS[entities.CURRENT_EFFECTS] # string, IE OFF or DAY
        
        return getattr(entities, effect_name, 'DAY') # dict

    def make_static_effect(self, effect_params):

        self.set_pwm_values(effect_params, 0)
        set_switch_status(effect_params, 0)
        self.set_led_values()

    def make_animated_effect(self, effect_params):

        self.duration_ticks = get_effect_duration(effect_params)
        print(self.duration_ticks)
        self.duration_midpoint = int(self.duration_ticks / 2)
        self.loop = effect_params['loop']
        make_animation_matrix(effect_params)
        set_switch_status(effect_params, 0)

    def set_pwm_values(self, effect_params, index=0):

        x = effect_params['red'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['RED'] = x
        x = effect_params['green'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['GREEN'] = x
        x = effect_params['blue'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['BLUE'] = x
        x = effect_params['warm'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['WARM'] = x
        x = effect_params['cool'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['COOL'] = x

    def set_led_values(self):

        entities.PWM(entities.PIN(entities.PICO_PIN['RED'])).duty_u16(int(entities.PWM_VALUES['RED']))
        entities.PWM(entities.PIN(entities.PICO_PIN['GREEN'])).duty_u16(int(entities.PWM_VALUES['GREEN']))
        entities.PWM(entities.PIN(entities.PICO_PIN['BLUE'])).duty_u16(int(entities.PWM_VALUES['BLUE']))
        entities.PWM(entities.PIN(entities.PICO_PIN['WARM'])).duty_u16(int(entities.PWM_VALUES['WARM']))
        entities.PWM(entities.PIN(entities.PICO_PIN['COOL'])).duty_u16(int(entities.PWM_VALUES['COOL']))

    def increment_effect(self):
        #print(self.current_tick)
        index = 0
        if self.current_tick > self.duration_midpoint:
            index = 1
            print('Midpoint')
        if self.current_tick > self.duration_ticks and self.loop:
            index = 0
            self.current_tick = 0
            print('loop')

        # set the pwm values here

        self.current_tick += entities.EFFECTS_TICK

# If this gets too big move it to model_effect.py

def make_animation_matrix(effect_params):
    '''
    format: red:(ticks, ticks), green(ticks, ticks), Etc
    '''
    pass

def get_effect_duration(effect_params):

    tick = entities.EFFECTS_TICK / 1000 # convert to seconds
    duration = effect_params['duration'] * 60 # seconds
    duration = duration / entities.CLOCK_RATIO # fast time in seconds
    random = 1 - effect_params['random'] # need it to be non-zero
    duration_minimum = duration * random

    duration = entities.RANDOM.randint(int(duration_minimum), int(duration)) # seconds
    duration_ticks = duration / tick

    return int(duration_ticks)

def set_switch_status(effect_params, index=0):

    entities.PIN(entities.PICO_PIN['BANK0_S']).value(effect_params['bank0'][index])
    entities.PIN(entities.PICO_PIN['BANK1_S']).value(effect_params['bank1'][index])
    entities.PIN(entities.PICO_PIN['BANK2_S']).value(effect_params['bank2'][index])
    entities.PIN(entities.PICO_PIN['BANK3_S']).value(effect_params['bank3'][index])
    entities.PIN(entities.PICO_PIN['BANK4_S']).value(effect_params['bank4'][index])
    entities.PIN(entities.PICO_PIN['SCENIC_S']).value(effect_params['scenic'][index])