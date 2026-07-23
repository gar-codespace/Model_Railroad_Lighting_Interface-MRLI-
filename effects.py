'''
Creates and runs both the animated and static effects.
'''

import entities
import model

class Effect():

    def __init__(self):

        self.effect_parameters: dict = {}
        self.red_pwm: int = 10000
        self.green_pwm: int = 10000
        self.blue_pwm: int = 10000
        self.warm_pwm: int = 10000
        self.white_pwm: int = 10000

        self.color_change_matrix: dict = {}
        self.duration_ticks: int = 100# the length of the effect in ticks
        self.duration_midpoint: int = 50
        self.current_tick: int = 0
        self.loop: bool = True
        self.animation_matrix: dict = {}

    def run_effect(self):
        self.make_effect()
        self.run_red_effect()
        self.run_green_effect()
        self.run_blue_effect()
        self.run_warm_effect()
        self.run_cool_effect()

    def make_effect(self):

        model.reset_clocks()
        model.get_highlighted_effect()
        self._get_effect_parameters()
        print(self.effect_parameters['type'])

        if self.effect_parameters['type'] == 'animated':
            pass
        else:
            self._set_pwm_values(0)
            self._set_led_values()

    def _get_effect_parameters(self):

        effect_name = entities.EFFECTS[entities.SELECTED_EFFECTS] # string, IE OFF or DAY
        self.effect_parameters = getattr(entities, effect_name, 'DAY') # dictionary, 'DAY' is the default

    def _set_pwm_values(self, index: int=0):

        x = self.effect_parameters['red'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['RED'] = x
        x = self.effect_parameters['green'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['GREEN'] = x
        x = self.effect_parameters['blue'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['BLUE'] = x
        x = self.effect_parameters['warm'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['WARM'] = x
        x = self.effect_parameters['cool'][index] * entities.PWM_STEPS
        entities.PWM_VALUES['COOL'] = x

    def _set_led_values(self):

        entities.PWM(entities.PIN(entities.PICO_PIN['RED'])).duty_u16(int(entities.PWM_VALUES['RED']))
        entities.PWM(entities.PIN(entities.PICO_PIN['GREEN'])).duty_u16(int(entities.PWM_VALUES['GREEN']))
        entities.PWM(entities.PIN(entities.PICO_PIN['BLUE'])).duty_u16(int(entities.PWM_VALUES['BLUE']))
        entities.PWM(entities.PIN(entities.PICO_PIN['WARM'])).duty_u16(int(entities.PWM_VALUES['WARM']))
        entities.PWM(entities.PIN(entities.PICO_PIN['COOL'])).duty_u16(int(entities.PWM_VALUES['COOL']))

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