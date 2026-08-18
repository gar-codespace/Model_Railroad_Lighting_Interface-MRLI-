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

class Effect():

    def __init__(self):

        self.effect_parameters: dict = {}
        entities.STATIC_BUFFER = entities.STATIC

        self.duration_ticks: int = 100000# the length of the effect in ticks

        self.r = entities.PICO_PIN['RED']
        self.g = entities.PICO_PIN['GREEN']
        self.b = entities.PICO_PIN['BLUE']
        self.w = entities.PICO_PIN['WARM']
        self.c = entities.PICO_PIN['COOL']

    def run_ANIMATED_effect(self, index):

        effect = entities.MAIN_MENU.get(index)[0]

        print(index)
        
    def run_STATIC_effect(self, index):
        '''
        Runs any of the effects listed in the entities.STATIC dictionary.
        '''
        # static_matrix = entities.STATIC
        static_matrix = entities.STATIC_BUFFER
        self.update_buffer(index, static_matrix)
        self._set_led_banks()
        self._set_led_values()

    def update_buffer(self, index, static_matrix):
        
        entities.RED = static_matrix['RED'][index] * entities.PWM_STEPS
        entities.GREEN = static_matrix['GREEN'][index] * entities.PWM_STEPS
        entities.BLUE = static_matrix['BLUE'][index] * entities.PWM_STEPS
        entities.WARM = static_matrix['WARM'][index] * entities.PWM_STEPS
        entities.COOL = static_matrix['COOL'][index] * entities.PWM_STEPS

        entities.BANK_0 = static_matrix['BANK_0'][index]
        entities.BANK_1 = static_matrix['BANK_1'][index]
        entities.BANK_2 = static_matrix['BANK_2'][index]
        entities.BANK_3 = static_matrix['BANK_3'][index]
        entities.BANK_4 = static_matrix['BANK_4'][index]
        entities.SCENIC = static_matrix['SCENIC'][index]

    def _set_led_banks(self):
        '''Sets the led bank relays from the value in the buffer'''

        entities.PIN(entities.PICO_PIN['BANK_0_S']).value(entities.BANK_0)
        entities.PIN(entities.PICO_PIN['BANK_1_S']).value(entities.BANK_1)
        entities.PIN(entities.PICO_PIN['BANK_2_S']).value(entities.BANK_2)
        entities.PIN(entities.PICO_PIN['BANK_3_S']).value(entities.BANK_3)
        entities.PIN(entities.PICO_PIN['BANK_4_S']).value(entities.BANK_4)
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(entities.SCENIC)

    def _set_led_values(self):
        '''Sets the led pwm values from the value in the buffer'''

        entities.PWM(self.r).duty_u16(int(entities.RED))
        entities.PWM(self.g).duty_u16(int(entities.GREEN))
        entities.PWM(self.b).duty_u16(int(entities.BLUE))
        entities.PWM(self.w).duty_u16(int(entities.WARM))
        entities.PWM(self.c).duty_u16(int(entities.COOL))
