'''
This library creates and runs both animated and static lighting effects.
Static effects are all grouped together in one dictionary called entities.STATIC.
Animated effects are all grouped together in one dictionary called entities.ANIMATED.

In the dictionary for each effect, the duration of the effect is given in real time minutes,
the time the effect actually takes in the real world.
The duration is then adjusted for model railroad 'scale' and converted to milliseconds.
The adjusted duration in milliseconds is expressed as ticks.

The duration of STATIC effects is defined as 0, since 'infinately long' seems rediculous.
'''

import entities
import model

class Effect():

    def __init__(self):

        self.effect_parameters: dict = {}

        self.duration_ticks: int = 100000# the length of the effect in ticks

        self.r = entities.PICO_PIN['RED']
        self.g = entities.PICO_PIN['GREEN']
        self.b = entities.PICO_PIN['BLUE']
        self.w = entities.PICO_PIN['WARM']
        self.c = entities.PICO_PIN['COOL']

    def run_STATIC_effect(self, index):
        '''
        Runs any of the effects listed in the entities.STATIC dictionary.
        '''

        effect_matrix = entities.STATIC
        self._set_led_banks(index, effect_matrix)
        self._set_pwm_values(index, effect_matrix)
        self._set_led_values()
        self._set_scenic_lights(index, effect_matrix)

    def run_ANIMATED_effect(self, index):

        effect = entities.MAIN_MENU.get(index)[0]

        print(index)
        
    def _set_led_banks(self, index, effect):

        x = effect.get('BANK0')[index]
        entities.PIN(entities.PICO_PIN['BANK0_S']).value(x)
        x = effect.get('BANK1')[index]
        entities.PIN(entities.PICO_PIN['BANK1_S']).value(x)
        x = effect.get('BANK2')[index]
        entities.PIN(entities.PICO_PIN['BANK2_S']).value(x)
        x = effect.get('BANK3')[index]
        entities.PIN(entities.PICO_PIN['BANK3_S']).value(x)
        x = effect.get('BANK4')[index]
        entities.PIN(entities.PICO_PIN['BANK4_S']).value(x)

    def _set_pwm_values(self, index, effect):

        entities.PWM_VALUES['RED'] = effect.get('RED')[index] * entities.PWM_STEPS
        entities.PWM_VALUES['GREEN'] = effect.get('GREEN')[index] * entities.PWM_STEPS
        entities.PWM_VALUES['BLUE'] = effect.get('BLUE')[index] * entities.PWM_STEPS
        entities.PWM_VALUES['WARM'] = effect.get('WARM')[index] * entities.PWM_STEPS
        entities.PWM_VALUES['COOL'] = effect.get('COOL')[index] * entities.PWM_STEPS

    def _set_led_values(self):

        entities.PWM(self.r).duty_u16(int(entities.PWM_VALUES['RED']))
        entities.PWM(self.g).duty_u16(int(entities.PWM_VALUES['GREEN']))
        entities.PWM(self.b).duty_u16(int(entities.PWM_VALUES['BLUE']))
        entities.PWM(self.w).duty_u16(int(entities.PWM_VALUES['WARM']))
        entities.PWM(self.c).duty_u16(int(entities.PWM_VALUES['COOL']))

    def _set_scenic_lights(self, index, effect):

        x = effect.get('SCENIC')[index]
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(x)
