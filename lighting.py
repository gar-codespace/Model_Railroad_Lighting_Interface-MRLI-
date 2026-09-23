'''
This library creates and runs both animated and static lighting effects.
Static effects are all grouped together in one dictionary called entities.SINGLES.
Each animated effect gets its own dictionary.
'''

import entities
import model

def run_startup_effect(): # Special case, runs only on startup.
    '''Effect fades up LEDs from dark (STATIC.Stby) to the the values of HILIGHTED_EFFECT.'''

    begin_index = 0
    end_index = entities.CURRENT_EFFECT[2]

    entities.WORKING_BUFFER = entities.SINGLES
    entities.WP_DUR = entities.STARTUP_EFFECT_LENGTH / entities.DEFAULT_CYCLE
    entities.NEXT_WP = end_index
    entities.SFX_GRP =  entities.WORKING_BUFFER['GROUP'][end_index]

    set_up_colors(begin_index)
    set_led_values()
    set_up_banks(end_index)
    set_led_banks()

    model.get_color_steps(begin_index)
    while entities.WP_DUR > 0:

        model.increment_colors()
        set_led_values()

        entities.UTIME.sleep_ms(entities.DEFAULT_CYCLE)

def set_up_effect():
    '''Load initial values into the Working Buffer.'''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.WORKING_BUFFER = entities.SINGLES
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
    get_sfx_group(index)
    if not current_waypoint_name == entities.WP_NAME:
        print(f'Current effect waypoint: {entities.WP_NAME}')
        print(f'Current sound fx group: {entities.SFX_GRP}')

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

########## VISUAL EFFECTS ###########
'''
For now there is only one but there could be more.
'''

def run_bolt():
    '''
    Simulated lightning.
    sub_set is a list of random length between 5 and 10 made up
    from randomly selected tuples from entities.LIGHTNING
    '''

# create a list of random length
    sample_count = len(entities.LIGHTNING) - 1 # The number of entries in entities.LIGHTNING
    sub_set_length = entities.RANDINT(5, 10) # A random number for the length of the subset
    sub_set = []
# Populate the random list with randomly chosen tuples.
    for _ in range(0, sub_set_length):
        pick_one = entities.RANDINT(0, sample_count) # Random integer
        sub_set.append(entities.LIGHTNING[pick_one]) # An entry from entities.LIGHTNING picked at random

# Run the randomly created list
    c = entities.PICO_PIN['COOL']
    for i in sub_set:

        entities.PWM(c).duty_u16(int(i[0]))
        entities.UTIME.sleep_ms(i[1])

    print(sub_set)
    