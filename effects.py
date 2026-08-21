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
        entities.STATIC_BUFFER = entities.STATIC

        self.duration_ticks: int = 100000# the length of the effect in ticks

        self.r = entities.PICO_PIN['RED']
        self.g = entities.PICO_PIN['GREEN']
        self.b = entities.PICO_PIN['BLUE']
        self.w = entities.PICO_PIN['WARM']
        self.c = entities.PICO_PIN['COOL']

    def update_buffer(self, index, effect_matrix):
        
        entities.RED = effect_matrix['RED'][index] * entities.PWM_STEPS
        entities.GREEN = effect_matrix['GREEN'][index] * entities.PWM_STEPS
        entities.BLUE = effect_matrix['BLUE'][index] * entities.PWM_STEPS
        entities.WARM = effect_matrix['WARM'][index] * entities.PWM_STEPS
        entities.COOL = effect_matrix['COOL'][index] * entities.PWM_STEPS

        entities.BANK_0 = effect_matrix['BANK_0'][index]
        entities.BANK_1 = effect_matrix['BANK_1'][index]
        entities.BANK_2 = effect_matrix['BANK_2'][index]
        entities.BANK_3 = effect_matrix['BANK_3'][index]
        entities.BANK_4 = effect_matrix['BANK_4'][index]
        entities.SCENIC = effect_matrix['SCENIC'][index]

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

    def _set_led_values(self):
        '''Sets the led pwm values from the value in the buffer'''

        entities.PWM(self.r).duty_u16(int(entities.RED))
        entities.PWM(self.g).duty_u16(int(entities.GREEN))
        entities.PWM(self.b).duty_u16(int(entities.BLUE))
        entities.PWM(self.w).duty_u16(int(entities.WARM))
        entities.PWM(self.c).duty_u16(int(entities.COOL))

    def run_STANDBY_effect(self):

        index = 0
        buffer = entities.STATIC_BUFFER

        self.update_buffer(index, buffer)
        self.set_led_banks()
        self._set_led_values()

    def run_STATIC_effect(self):
        '''
        Runs any of the effects listed in the entities.STATIC dictionary.
        '''
        index = entities.CURRENT_EFFECT[2]
        buffer = entities.STATIC_BUFFER

        self.update_buffer(index, buffer)
        self.set_led_banks()
        self._set_led_values()

    def run_ANIMATED_effect(self):

        print(entities.CURRENT_EFFECT)

        index = entities.CURRENT_EFFECT[2]
    # Copy the selected effect matrix into ANIMATED_BUFFER
        entities.ANIMATED_BUFFER = getattr(entities, entities.CURRENT_EFFECT[1])
        buffer = entities.ANIMATED_BUFFER
    # Set the LEDs and banks to their initial value.
        self.effect.update_buffer(index, buffer)
        self.effect.set_led_banks()
        self.effect._set_led_values()
    # waypoint_duration is the number of times the effect will loop, given a delay of entities.CLOCK_CYCLE
        waypoint_duration = model.get_waypoint_duration(index)
    # get the change per cycle for each color
        entities.STEP_R = model.get_color_delta(index, 'RED') / waypoint_duration
        entities.STEP_G = model.get_color_delta(index, 'GREEN') / waypoint_duration
        entities.STEP_B = model.get_color_delta(index, 'BLUE') / waypoint_duration
        entities.STEP_W = model.get_color_delta(index, 'WARM') / waypoint_duration
        entities.STEP_C = model.get_color_delta(index, 'COOL') / waypoint_duration

        while waypoint_duration > 0:

            waypoint_duration -= 1
            entities.RED = entities.RED + entities.STEP_R
            entities.GREEN =entities.GREEN + entities.STEP_G
            entities.BLUE = entities.BLUE + entities.STEP_B
            entities.WARM = entities.WARM + entities.STEP_W
            entities.COOL = entities.COOL + entities.STEP_C

            self.effect._set_led_values()