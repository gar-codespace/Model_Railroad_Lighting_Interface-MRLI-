'''
Creates and runs both animated and static lighting effects.
Static effects are all grouped together in one dictionary called STATIC.
'''
'''
Write about how animated effects work.
In the dictionary for each effect, the length is given in real time minutes, the time the effect
actually takes in the real world.
The length is then adjusted for model railroad 'scale' and converted to milliseconds.
'''
'''
TODO:
Explain what a tick is
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

    def run_static_effect(self, index):
        '''
        Runs any of the effects listed in the entities.STATIC dictionary.
        '''

        effect_matrix = entities.STATIC
        self._set_led_banks(index, effect_matrix)
        self._set_pwm_values(index, effect_matrix)
        self._set_led_values()
        self._set_scenic_lights(index, effect_matrix)

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





############## THE OLD CODE  ###################

    def run_effect(self, index, effect):

        if effect.get('TIME')[index] == 0:
            loops = 1
        else:
            loops = len(effect.get('INDEX'))

        for i in range(loops):

            duration = self._get_duration(i, effect)
            r_delta = self._get_color_change(i, effect.get('RED'))
            g_delta = self._get_color_change(i, effect.get('GREEN'))
            b_delta = self._get_color_change(i, effect.get('BLUE'))
            w_delta = self._get_color_change(i, effect.get('WARM'))
            c_delta = self._get_color_change(i, effect.get('COOL'))


        duration = 1000
        while True:


            entities.LED.toggle()

            await entities.ASYNCIO.sleep_ms(100) # 2 seconds





    def _get_color_change(self, index, effect):

        pass


    def _get_duration(self, index, effect):

        start = effect.get('TIME')[index]
        try:
            end = effect.get('TIME')[index + 1]
        except:
            end = 0

        duration = end - start # minutes
        duration = duration * 60 * 1000 # milliseconds

        return duration



    def run_red_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.RED_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('red led effect finished')










    def set_led_banks(self):

        entities.PIN(entities.PICO_PIN['BANK0_S']).value(self.effect_parameters['bank0'])
        entities.PIN(entities.PICO_PIN['BANK1_S']).value(self.effect_parameters['bank1'])
        entities.PIN(entities.PICO_PIN['BANK2_S']).value(self.effect_parameters['bank2'])
        entities.PIN(entities.PICO_PIN['BANK3_S']).value(self.effect_parameters['bank3'])
        entities.PIN(entities.PICO_PIN['BANK4_S']).value(self.effect_parameters['bank4'])

    def run_effectx(self):

        self.effect_setup()
        self.make_effect()
        self.run_color_effects()

    def run_color_effects(self):

        self.run_red_effect()
        self.run_green_effect()
        self.run_blue_effect()
        self.run_warm_effect()
        self.run_cool_effect()

    def effect_setup(self):

        model.reset_clocks()
        model.get_highlighted_effect()
        self._get_effect_parameters()
        self._set_effect_type()

    def make_effect(self):
        if entities.EFFECT_TYPE == 'ANIMATED':
            pass
        else:
            self._set_pwm_values()
            self._set_led_values()
            self.set_led_banks()

    def _get_effect_parameters(self):

        effect_name = entities.EFFECTS[entities.SELECTED_EFFECT] # string, IE OFF or DAY
        self.effect_parameters = getattr(entities, effect_name, 'DAY') # dictionary, 'DAY' is the default

    def _set_effect_type(self):

        entities.EFFECT_TYPE = self.effect_parameters['type']

    def _set_pwm_valuesx(self, index: int=0):

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



    def set_led_banks(self):

        entities.PIN(entities.PICO_PIN['BANK0_S']).value(self.effect_parameters['bank0'])
        entities.PIN(entities.PICO_PIN['BANK1_S']).value(self.effect_parameters['bank1'])
        entities.PIN(entities.PICO_PIN['BANK2_S']).value(self.effect_parameters['bank2'])
        entities.PIN(entities.PICO_PIN['BANK3_S']).value(self.effect_parameters['bank3'])
        entities.PIN(entities.PICO_PIN['BANK4_S']).value(self.effect_parameters['bank4'])
        entities.PIN(entities.PICO_PIN['SCENIC_S']).value(self.effect_parameters['scenic'])

    # Color coroutine: runs the selected effect, one for each color
    def run_red_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.RED_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('red led effect finished')
        
    def run_green_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.GREEN_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('green led effect finished')

    def run_blue_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.BLUE_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay)
        
        print('blue led effect finished')

    def run_warm_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.WARM_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('warm led effect finished')

    def run_cool_effect(self):

        delay = entities.DEFAULT_TICK
        while entities.COOL_CLOCK > 0:
            pass

            await entities.ASYNCIO.sleep_ms(delay) #10 sec
        
        print('cool led effect finished')



# If this gets too big move it to model_effect.py

def make_animation_matrix(effect_params):
    '''
    format: red:(ticks, ticks), green(ticks, ticks), Etc
    '''
    pass

def get_effect_duration(effect_params):

    # tick = entities.EFFECTS_TICK / 1000 # convert to seconds
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