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
        entities.ANIMATED_BUFFER = entities.ANIMATED

        self.duration_ticks: int = 100000# the length of the effect in ticks

        self.r = entities.PICO_PIN['RED']
        self.g = entities.PICO_PIN['GREEN']
        self.b = entities.PICO_PIN['BLUE']
        self.w = entities.PICO_PIN['WARM']
        self.c = entities.PICO_PIN['COOL']

    def run_ANIMATED_effect(self, index):
        '''
        With this version the LED banks are not switched during the effect.
        They are set at the begining and that's it.
        '''

        '''
        

        3. Start the loop:
            3a. Get the duration until the next index.
                3a1. If the current index is the last index, use the first index as the next index.
            3b. Calculate the change (in PWM values) for each color.
            3c. Run the effect to the next index.
                3c1. Use the effect buffer to hold the incremental values.
        '''

    # Set the LEDs and banks to their initial value.
        self._update_buffer(index, entities.ANIMATED_BUFFER)
        self._set_led_banks()
        self._set_led_values()
   

    # Start the loop:
        # Get the duration of the way point
        duration = entities.ANIMATED_BUFFER['TIME'][index] # real time minutes
        duration = duration * 60 # real time seconds
        random = 1 - entities.ANIMATED_BUFFER['RANDOM'][index]
        xmax = duration # seconds
        xmin = duration * random # seconds
        duration = entities.RANDOM.randint(int(xmin), int(xmax)) # seconds
        duration = duration * 1000 # adjusted duration in milliseconds
        delay_ticks = int(duration / entities.CLOCK_CYCLE) # how long the while loop delays in ms
        print(delay_ticks)

        # find the next index
        # If the current index is the last index, use the first index as the next index.
        group = entities.ANIMATED_BUFFER['GROUP'][index]
        next_index = index + 1
        if not entities.ANIMATED_BUFFER['index'][index]:
            pass

        # get the change for each color
        # current = entities.ANIMATED_BUFFER['RED'][index]
        # target = entities.ANIMATED_BUFFER['RED'][next_index]
        # delta = current - target # decimal percentage, pos or neg
        # delta = delta * entities.PWM_STEPS
        # entities.STEP_R = delta / delay_ticks

        # while delay_ticks > 0:
        #     delay_ticks - 1
        #     entities.RED = int(entities.RED + entities.STEP_R)

        #     await entities.ASYNCIO.sleep_ms(entities.CLOCK_CYCLE)












    def run_STATIC_effect(self, index):
        '''
        Runs any of the effects listed in the entities.STATIC dictionary.
        '''

        self._update_buffer(index, entities.STATIC_BUFFER)
        self._set_led_banks()
        self._set_led_values()

    def _update_buffer(self, index, effect_matrix):
        
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
