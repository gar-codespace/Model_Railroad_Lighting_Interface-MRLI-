'''
This library creates and runs both animated and static lighting effects.
Static effects are all grouped together in one dictionary called entities.STATIC.
Each animated effect gets its own dictionary.
'''
'''
It's possible to confuse STATIC the lighting effect with STATIC the machine state.
Fix this.
'''

import entities
import model

def set_up_effect():
    '''Load initial values into the Working Buffer.'''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.WORKING_BUFFER = entities.STATIC
    else:
        entities.WORKING_BUFFER = getattr(entities, entities.CURRENT_EFFECT[1])
        entities.CLOCK_CYCLE = entities.WORKING_BUFFER['CLOCK_CYCLE']
        entities.CLOCK_OFFSET = entities.WORKING_BUFFER['CLOCK_OFFSET']

    index = entities.CURRENT_EFFECT[2]
    lighting_effect_boiler_plate(index)

def set_next_waypoint():

    index = entities.NEXT_WP
    lighting_effect_boiler_plate(index)

def lighting_effect_boiler_plate(index):
    '''Common to set_up_effect and set_next_waypoint.'''

    current_waypoint_name = entities.WP_NAME
    get_waypoint_name(index)
    if not current_waypoint_name == entities.WP_NAME:
        print(f'Current effect waypoint: {entities.WP_NAME}')

    set_up_colors(index)
    set_up_banks(index)

    model.get_waypoint_duration(index)
    model.get_next_waypoint(index)
    model.get_color_steps(index)

    set_led_banks()
    set_led_values()

def get_waypoint_name(index):

    entities.WP_NAME = entities.WORKING_BUFFER['NAME'][index]

def get_sfx_group(index):

    entities.SFX_GRP = entities.WORKING_BUFFER['GROUP'][index]

def set_up_colors(index):
    
    entities.RED   = int(entities.WORKING_BUFFER['RED'][index] * entities.PWM_STEPS)
    entities.GREEN = int(entities.WORKING_BUFFER['GREEN'][index] * entities.PWM_STEPS)
    entities.BLUE  = int(entities.WORKING_BUFFER['BLUE'][index] * entities.PWM_STEPS)
    entities.WARM  = int(entities.WORKING_BUFFER['WARM'][index] * entities.PWM_STEPS)
    entities.COOL  = int(entities.WORKING_BUFFER['COOL'][index] * entities.PWM_STEPS)

def set_up_banks(index):

    entities.BANK_0 = entities.WORKING_BUFFER['BANK_0'][index]
    entities.BANK_1 = entities.WORKING_BUFFER['BANK_1'][index]
    entities.BANK_2 = entities.WORKING_BUFFER['BANK_2'][index]
    entities.BANK_3 = entities.WORKING_BUFFER['BANK_3'][index]
    entities.BANK_4 = entities.WORKING_BUFFER['BANK_4'][index]
    entities.SCENIC = entities.WORKING_BUFFER['SCENIC'][index]

def set_led_banks():
    '''Sets the led bank relays from the value in the buffer.'''

    entities.PIN(entities.PICO_PIN['BANK_0_R']).value(entities.BANK_0)
    entities.PIN(entities.PICO_PIN['BANK_1_R']).value(entities.BANK_1)
    entities.PIN(entities.PICO_PIN['BANK_2_R']).value(entities.BANK_2)
    entities.PIN(entities.PICO_PIN['BANK_3_R']).value(entities.BANK_3)
    entities.PIN(entities.PICO_PIN['BANK_4_R']).value(entities.BANK_4)
    entities.PIN(entities.PICO_PIN['SCENIC_R']).value(entities.SCENIC)

def set_led_values():
    '''Sets the led pwm values from the value in the Effect Buffer.'''

    r = entities.PICO_PIN['RED']
    g = entities.PICO_PIN['GREEN']
    b = entities.PICO_PIN['BLUE']
    w = entities.PICO_PIN['WARM']
    c = entities.PICO_PIN['COOL']

    entities.PWM(r).duty_u16(int(entities.RED))
    entities.PWM(g).duty_u16(int(entities.GREEN))
    entities.PWM(b).duty_u16(int(entities.BLUE))
    entities.PWM(w).duty_u16(int(entities.WARM))
    entities.PWM(c).duty_u16(int(entities.COOL))

def shut_off_led_banks():

    entities.PIN(entities.PICO_PIN['BANK_0_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_1_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_2_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_3_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_4_R']).value(0)
    entities.PIN(entities.PICO_PIN['SCENIC_R']).value(0)
