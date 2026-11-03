'''
Static effects are all grouped together in one dictionary called entities.SINGLES.
Each animated effect gets its own dictionary.
Special VFX functions are here as well.
'''

import entities
import model

def fade_up_lights():
    '''
    Edge case, runs only on startup.
    This effect fades up LEDs from dark (SINGLES.Dark) to the the values of entities.CURRENT_EFFECT.
    '''

    begin_index = 0
    end_index = entities.CURRENT_EFFECT[2]

    entities.WORKING_BUFFER = entities.SINGLES
    entities.WP_DUR = entities.STARTUP_EFFECT_DURATION / entities.DEFAULT_CYCLE
    entities.NEXT_WP = end_index
    entities.CLIP_G =  entities.WORKING_BUFFER['GROUP'][end_index]

    set_color_values(begin_index)
    set_pwm_values()
    set_up_banks(end_index)
    set_bank_relays()

    model.get_color_steps(begin_index)
    while entities.WP_DUR > 0:

        model.increment_waypoint()
        set_pwm_values()

        entities.UTIME.sleep_ms(entities.DEFAULT_CYCLE)

def set_up_effect():
    '''Load initial values into the Working Buffer.'''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.WORKING_BUFFER = entities.SINGLES
    else:
        entities.WORKING_BUFFER = getattr(entities, entities.CURRENT_EFFECT[1])
        entities.CLOCK_CYCLE = entities.WORKING_BUFFER['CLOCK_CYCLE']
        entities.CLOCK_OFFSET = entities.WORKING_BUFFER['CLOCK_OFFSET']

    entities.CUR_WP = entities.CURRENT_EFFECT[2]

    lighting_effect_boiler_plate(entities.CUR_WP)

def set_next_waypoint():

    lighting_effect_boiler_plate(entities.NEXT_WP)

def lighting_effect_boiler_plate(index):
    '''Common to set_up_effect and set_next_waypoint.'''

    current_waypoint_name = entities.WP_NAME
    get_waypoint_name(index)
    get_sfx_group(index)
    get_hour(index)

    if not current_waypoint_name == entities.WP_NAME:
        entities.PROGRESS_MESSAGE = f'Waypoint Run Time: {entities.WAYPOINT_RUN_TIME} (sec)\n\
New Waypoint: {entities.WP_NAME}\n\
Sound Group: {entities.CLIP_G}'

    set_color_values(index)
    set_up_banks(index)

    model.get_waypoint_duration(index)
    model.get_next_waypoint(index)
    model.get_color_steps(index)
    model.get_hour_steps()

    set_bank_relays()
    set_pwm_values()

def get_waypoint_name(index):

    entities.WP_NAME = entities.WORKING_BUFFER['NAME'][index]

def get_sfx_group(index):

    entities.CLIP_G = entities.WORKING_BUFFER['GROUP'][index]

def get_hour(index):

    entities.HOUR = entities.WORKING_BUFFER['HOUR'][index]
    entities.TIME = entities.WORKING_BUFFER['TIME'][index]

def set_color_values(index):
    
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

def set_bank_relays():

    entities.PIN(entities.PICO_PIN['BANK_0_R']).value(entities.BANK_0)
    entities.PIN(entities.PICO_PIN['BANK_1_R']).value(entities.BANK_1)
    entities.PIN(entities.PICO_PIN['BANK_2_R']).value(entities.BANK_2)
    entities.PIN(entities.PICO_PIN['BANK_3_R']).value(entities.BANK_3)
    entities.PIN(entities.PICO_PIN['BANK_4_R']).value(entities.BANK_4)
    entities.PIN(entities.PICO_PIN['SCENIC_R']).value(entities.SCENIC)

def set_pwm_values():

    pin = entities.PICO_PIN['RED']
    entities.PWM(pin).duty_u16(int(entities.RED))
    pin = entities.PICO_PIN['GREEN']
    entities.PWM(pin).duty_u16(int(entities.GREEN))
    pin = entities.PICO_PIN['BLUE']
    entities.PWM(pin).duty_u16(int(entities.BLUE))
    pin = entities.PICO_PIN['WARM']
    entities.PWM(pin).duty_u16(int(entities.WARM))
    pin = entities.PICO_PIN['COOL']
    entities.PWM(pin).duty_u16(int(entities.COOL))

def set_banks_to_0():

    entities.PIN(entities.PICO_PIN['BANK_0_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_1_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_2_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_3_R']).value(0)
    entities.PIN(entities.PICO_PIN['BANK_4_R']).value(0)
    entities.PIN(entities.PICO_PIN['SCENIC_R']).value(0)

################ visual effects method #################

def run_vfx():
    '''Runs the associated visual effect if it exists.
    Sound effects trigger visual effects.
    '''

    vfx = entities.AMBIENCE[entities.CLIP][3]

    try:
        attrib = f'run_{vfx}'
        getattr(VFX, attrib)() # IE run_bolt()
        entities.PROGRESS_MESSAGE = f'Visual Effect: {vfx}'
    except:
        pass

########## VISUAL EFFECTS ###########
'''
Putting the VFX in class VFX is the easy way to get getattr(VFX, attrib)() to work.
Additional visual effects can be added to this class.
'''

class VFX:

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
        for _ in range(sub_set_length):
            pick_one = entities.RANDINT(0, sample_count) # Random integer
            sub_set.append(entities.LIGHTNING[pick_one]) # An entry from entities.LIGHTNING picked at random

    # Run the randomly created list
        c = entities.PICO_PIN['COOL']
        for i in sub_set:

            entities.PWM(c).duty_u16(int(i[0]))
            entities.UTIME.sleep_ms(i[1])
    