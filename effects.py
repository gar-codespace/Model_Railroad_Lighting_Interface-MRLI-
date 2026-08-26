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

        entities.STATIC_BUFFER = entities.STATIC
        self.effect_dictionary: dict = {}

        self.r = entities.PICO_PIN['RED']
        self.g = entities.PICO_PIN['GREEN']
        self.b = entities.PICO_PIN['BLUE']
        self.w = entities.PICO_PIN['WARM']
        self.c = entities.PICO_PIN['COOL']

    def set_up_colors(self, index, effect_dictionary):
        
        entities.RED   = int(effect_dictionary['RED'][index] * entities.PWM_STEPS)
        entities.GREEN = int(effect_dictionary['GREEN'][index] * entities.PWM_STEPS)
        entities.BLUE  = int(effect_dictionary['BLUE'][index] * entities.PWM_STEPS)
        entities.WARM  = int(effect_dictionary['WARM'][index] * entities.PWM_STEPS)
        entities.COOL  = int(effect_dictionary['COOL'][index] * entities.PWM_STEPS)

    def set_up_banks(self, index, effect_dictionary):

        entities.BANK_0 = effect_dictionary['BANK_0'][index]
        entities.BANK_1 = effect_dictionary['BANK_1'][index]
        entities.BANK_2 = effect_dictionary['BANK_2'][index]
        entities.BANK_3 = effect_dictionary['BANK_3'][index]
        entities.BANK_4 = effect_dictionary['BANK_4'][index]
        entities.SCENIC = effect_dictionary['SCENIC'][index]

    def set_led_banks(self):
        '''Sets the led bank relays from the value in the buffer'''

        entities.PIN(entities.PICO_PIN['BANK_0_S']).value(entities.BANK_0)
        entities.PIN(entities.PICO_PIN['BANK_1_S']).value(entities.BANK_1)
        entities.PIN(entities.PICO_PIN['BANK_2_S']).value(entities.BANK_2)
        entities.PIN(entities.PICO_PIN['BANK_3_S']).value(entities.BANK_3)
        entities.PIN(entities.PICO_PIN['BANK_4_S']).value(entities.BANK_4)
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(entities.SCENIC)

    def shut_off_leds(self):

        entities.PIN(entities.PICO_PIN['BANK_0_S']).value(0)
        entities.PIN(entities.PICO_PIN['BANK_1_S']).value(0)
        entities.PIN(entities.PICO_PIN['BANK_2_S']).value(0)
        entities.PIN(entities.PICO_PIN['BANK_3_S']).value(0)
        entities.PIN(entities.PICO_PIN['BANK_4_S']).value(0)
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(0)

    def set_led_values(self):
        '''Sets the led pwm values from the value in the buffer'''

        entities.PWM(self.r).duty_u16(int(entities.RED))
        entities.PWM(self.g).duty_u16(int(entities.GREEN))
        entities.PWM(self.b).duty_u16(int(entities.BLUE))
        entities.PWM(self.w).duty_u16(int(entities.WARM))
        entities.PWM(self.c).duty_u16(int(entities.COOL))

    def set_up_effect(self):
        '''
        Load initial values into the Effect Buffer.
        '''

        if entities.CURRENT_EFFECT[1] == 'STATIC':
            self.effect_dictionary = entities.STATIC_BUFFER
        else:
            entities.ANIMATED_BUFFER = getattr(entities, entities.CURRENT_EFFECT[1])
            self.effect_dictionary = entities.ANIMATED_BUFFER

        index = entities.CURRENT_EFFECT[2]
        self.effect_boiler_plate(index)

    def set_next_waypoint(self):

        index = entities.NEXT_WP
        self.effect_boiler_plate(index)

    def effect_boiler_plate(self, index):
        '''
        Common to set_up_effect and set_next_waypoint
        '''

        self.set_up_colors(index, self.effect_dictionary)
        self.set_up_banks(index, self.effect_dictionary)
        model.get_waypoint_duration(index)
        model.get_next_waypoint(index)
        entities.STEP_R = model.get_color_delta(index, 'RED') / entities.WP_DUR
        entities.STEP_G = model.get_color_delta(index, 'GREEN') / entities.WP_DUR
        entities.STEP_B = model.get_color_delta(index, 'BLUE') / entities.WP_DUR
        entities.STEP_W = model.get_color_delta(index, 'WARM') / entities.WP_DUR
        entities.STEP_C = model.get_color_delta(index, 'COOL') / entities.WP_DUR

        self.set_led_banks()
        self.set_led_values()

    def EDIT_turn_left(self):

        index = entities.CURRENT_EFFECT[2]
        color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]

        print('EDIT_turn_left')

        entities.STATIC_BUFFER[color][index] = model.pwm2percent(getattr(entities, color))