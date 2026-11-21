'''
Model Railroad Lighting Interface (MRLI)
The push button driver library is imported here.
The rotary encoder driver library is imported here.
'''

import entities
import states


def logger():
      '''Write machine progress somewhere, screen, log, Etc.'''

      if not entities.LOGGING_MESSAGE:
            return

      for message in entities.LOGGING_MESSAGE:
            print(message)

      entities.LOGGING_MESSAGE = []

################## MACHINE ######################

def set_relay_pins():
    '''The STEMMA relay from Adafruit.'''

    entities.PIN(entities.PICO_PIN['BANK_0_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_1_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_2_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_3_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_4_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['SCENIC_R'], entities.PIN.OUT)

def set_pwm_led_pins():

    entities.PWM(entities.PIN(entities.PICO_PIN['RED']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['WARM']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['COOL']), freq=entities.PWM_FREQ)

def get_button(pico_pin:int, params:dict, name:str) ->object:

    mode = getattr(entities.PIN, params['MODE'])
    pull = getattr(entities.PIN, params['PULL'])

    pin = entities.PIN(pico_pin, mode=mode, pull=pull)

    driver = __import__(params['DRIVER']).Button

    return driver(params=params, pin=pin, name=name)

def get_encoder(pico_tra:int, pico_trb:int, pico_psh:int=None, params:dict={}) ->object:

    mode = getattr(entities.PIN, params['MODE'])
    pull = getattr(entities.PIN, params['PULL'])
    tra = entities.PIN(pico_tra, mode=mode, pull=pull)
    trb = entities.PIN(pico_trb, mode=mode, pull=pull)
    psh = entities.PIN(pico_psh, mode=mode, pull=pull)

    driver = __import__(params['DRIVER']).Encoder

    return driver(params=params, pin_clk=trb, pin_dt=tra, pin_sw=psh)

################## DISPLAY LISTS ######################

def get_menu_first_item():
    '''Abstracted to adjust for effects menu layout changes.'''

    index_double = _get_index_double()

    position = len(entities.EFFECTS_MENU) + entities.EFFECTS_HILIGHTED_EFFECT
    entities.EFFECTS_MENU_FIRST_ITEM = index_double[position - entities.EFFECTS_HIGHLIGHT_ROW]

def get_welcome_list() -> list:

    welcome_list: list = []
    char_per_row = entities.MAIN_FORMAT['CHAR_PER_ROW']
    line_format = f'^{char_per_row}s'

    for i in range(entities.MAIN_FORMAT['ROWS']):
        try:
            welcome_list.append(f'{entities.WELCOME_SCREEN[i]:{line_format}}')
        except:
            welcome_list.append('')

    return welcome_list

def get_effects_list() -> list:
    '''Returns a list of effects menu items.'''

    index_double = _get_index_double()
    index_subset = index_double[entities.EFFECTS_MENU_FIRST_ITEM:] # it's only important to chop the beginning
    entities.EFFECTS_HILIGHTED_EFFECT = index_subset[entities.EFFECTS_HIGHLIGHT_ROW]

    menu_list: list = []
    for i in range(entities.MAIN_FORMAT['ROWS']):
        line_prefix = entities.EFFECTS_MENU_ANIMATED_SYMBOL
        if entities.EFFECTS_MENU.get(index_subset[i])[1] == 'SINGLES':
            line_prefix = entities.EFFECTS_MENU_STATIC_SYMBOL
        line = f'{line_prefix} {entities.EFFECTS_MENU.get(index_subset[i])[0]}'
        menu_list.append(line)

    return menu_list

def get_status_list() -> list:
    '''The status screen is displayed when the machine state is ANIMATED, STATIC, or EDIT.'''

    status_screen: list = []

    # The first line can change, depending on the machine state
    attrib = f'{entities.MACHINE_STATE}_first_line'
    first_line = getattr(states, attrib)() # IE animated_first_line()

    status_screen.append(first_line)
    
    value = pwm_percent(entities.RED)
    status_screen.append(f'  Red: {value:.4%}')

    value = pwm_percent(entities.GREEN)
    status_screen.append(f'Green: {value:.4%}')

    value = pwm_percent(entities.BLUE)
    status_screen.append(f' Blue: {value:.4%}')

    value = pwm_percent(entities.WARM)
    status_screen.append(f' Warm: {value:.4%}')

    value = pwm_percent(entities.COOL)
    status_screen.append(f' Cool: {value:.4%}')

    return status_screen

def get_empty_list() -> list:

    return ['' for _ in range(entities.MAIN_FORMAT['ROWS'])]

def pwm_percent(pwm) ->float:
    '''Convert a pwm value to decimal percentage.'''

    return pwm / entities.PWM_STEPS

def _get_index_double() ->tuple:
    '''IE (0, 1, 2, 3, 4, 0, 1, 2, 3 , 4)'''
    
    index_double = tuple(range(len(entities.EFFECTS_MENU)))
    index_double = index_double + index_double

    return index_double

################## SOUND CLIPS ######################

def get_ambient_clip() -> tuple:
    '''Randomly pick a sound clip from the ambient sounds group.'''
    
    ambient_group = getattr(entities, entities.CLIP_G)
    select = entities.RANDINT(0, len(ambient_group) - 1)

    entities.CLIP = ambient_group[select]
    entities.LOGGING_MESSAGE.append(f'Sound Clip: {entities.AMBIENCE[entities.CLIP][2]}')

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad


################## LIGHTING EFFECTS ######################

def get_waypoint_duration(index):
    '''The duration of the waypoint is the number of times the 'while loop' is run.'''

    if entities.CURRENT_EFFECT[1] == 'SINGLES':
        entities.WP_DUR = 1
    else:
    # Convert duration to milliseconds
        duration = entities.WORKING_BUFFER['TIME'][index] # real time minutes
        duration *= 60 # real time seconds
        duration *= 1000 # real time milliseconds

    # Adjustment for asyncio overhead
        duration *= entities.CLOCK_OFFSET 

    # Apply the random factor
        random = entities.WORKING_BUFFER['RANDOM'][index]
        d_max = duration # milliseconds
        d_min = duration * (random) # milliseconds
        duration = entities.RANDINT(int(d_max - d_min), int(d_max)) # milliseconds

    # Scale the duration for model railroads
        duration /= entities.FAST_TIME_CLOCK # milliseconds

    # The waypoint duration expressed in cycles
        entities.WP_DUR = int(duration / entities.CLOCK_CYCLE) # milliseconds / ms per cycle = cycles

def get_next_waypoint(index):

    if entities.CURRENT_EFFECT[1] == 'SINGLES':
        entities.NEXT_WP = entities.CURRENT_EFFECT[2]

    else:
        next_index = index + 1
        if next_index == len(entities.WORKING_BUFFER['TIME']):
            next_index = 0

        entities.NEXT_WP = int(next_index)

def get_color_steps(index):
    '''How much each pwm color changes per cycle.'''
    
    entities.STEP_R = _get_color_delta(index, 'RED') / entities.WP_DUR
    entities.STEP_G = _get_color_delta(index, 'GREEN') / entities.WP_DUR
    entities.STEP_B = _get_color_delta(index, 'BLUE') / entities.WP_DUR
    entities.STEP_W = _get_color_delta(index, 'WARM') / entities.WP_DUR
    entities.STEP_C = _get_color_delta(index, 'COOL') / entities.WP_DUR

def _get_color_delta(index:int, color:str):
    '''
    The value each color changes between waypoints expressed im PWM steps.
    Can return zero, a positive or negative value.
    '''

    color_begin = entities.WORKING_BUFFER[color][index] # decimal percent
    color_end = entities.WORKING_BUFFER[color][entities.NEXT_WP] # decimal percent
    color_delta = color_begin - color_end # decimal percent
    color_delta *= entities.PWM_STEPS # pwm steps

    return int(color_delta)

def get_hour_steps():
    '''Display the time of day.'''

    if entities.WORKING_BUFFER['HOUR'][entities.CUR_WP]:
        entities.STEP_H = (entities.TIME / entities.WP_DUR) / 60
    else:
        entities.STEP_H = 0

def increment_waypoint():

        entities.RED -= entities.STEP_R
        entities.GREEN -= entities.STEP_G
        entities.BLUE -= entities.STEP_B
        entities.WARM -= entities.STEP_W
        entities.COOL -= entities.STEP_C

        entities.HOUR += entities.STEP_H
        entities.WP_DUR -= 1

################## SERIAL PROTOCOLS ######################

def get_i2c(params):
    '''I2C is used for the display.'''

    sda = entities.PIN(entities.PICO_PIN[params['SDA']])
    scl = entities.PIN(entities.PICO_PIN[params['SCL']])
    id = params['ID']
    freq = params['FREQ']

    i2c = entities.I2C(id=id, sda=sda, scl=scl, freq=freq)
    entities.LOGGING_MESSAGE.append(f'{i2c}')

    return i2c

def get_spi(params):
    ...

def get_uart(params):

    try:
        tx = entities.PIN(entities.PICO_PIN[params['TX']])
    except:
        tx = None
    try:
        rx = entities.PIN(entities.PICO_PIN[params['RX']])
    except:
        rx = None

    id = params['ID']
    baud = params['FREQ']

    uart = entities.UART(id, baudrate=baud, tx=tx, rx=rx)
    entities.LOGGING_MESSAGE.append(f'{uart}')

    return uart
