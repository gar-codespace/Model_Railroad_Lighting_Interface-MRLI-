import entities


def set_relay_pins():
    '''The STEMMA relay from Adafruit that turns the led banks or scenic lighting on or off.'''

    entities.PIN(entities.PICO_PIN['BANK_0_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_1_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_2_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_3_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_4_R'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['SCENIC_R'], entities.PIN.OUT)

def set_pwm_led_pins():
    '''Initializes the PWM pins.'''

    entities.PWM(entities.PIN(entities.PICO_PIN['RED']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['WARM']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['COOL']), freq=entities.PWM_FREQ)

def pwm2percent(pwm):
    '''Convert a pwm value to decimal percentage rounded to 4 places.'''

    x = pwm / entities.PWM_STEPS
    y = x * 100
    return x

def get_index_double():
    '''IE [0, 1, 2, 3, 4, 0, 1, 2, 3 , 4]'''
    
    index_double = tuple(range(0, len(entities.MAIN_MENU)))
    index_double = index_double + index_double

    return index_double

def get_waypoint_duration(index):
    '''
    The duration of the waypoint is the number of times the while loop is run.
    When tested, the Picos clock was consistantly off from real time,
    due to the overhead from asyncio, so the CLOCK_OFFSET adjusts for that.
    '''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.WP_DUR = 1
    else: # Convert duration to milliseconds
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

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.NEXT_WP = entities.CURRENT_EFFECT[2]

    else:
        next_index = index + 1
        if next_index == len(entities.WORKING_BUFFER['TIME']):
            next_index = 0

        entities.NEXT_WP = int(next_index)

def get_color_steps(index):
    
    entities.STEP_R = get_color_delta(index, 'RED') / entities.WP_DUR
    entities.STEP_G = get_color_delta(index, 'GREEN') / entities.WP_DUR
    entities.STEP_B = get_color_delta(index, 'BLUE') / entities.WP_DUR
    entities.STEP_W = get_color_delta(index, 'WARM') / entities.WP_DUR
    entities.STEP_C = get_color_delta(index, 'COOL') / entities.WP_DUR

def get_color_delta(index:int, color:str):
    '''
    The value each color changes between waypoints expressed im PWM steps.
    Can return zero, a positive or negative value.
    '''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
       color_delta = 0

    else:
        color_begin = entities.WORKING_BUFFER[color][index] # decimal percent
        color_end = entities.WORKING_BUFFER[color][entities.NEXT_WP] # decimal percent
        color_delta = color_begin - color_end # decimal percent
        color_delta *= entities.PWM_STEPS # pwm steps

    return int(color_delta)

def get_menu_first_item():
    '''Abstracted to adjust for menu layout changes.'''

    index_double = get_index_double()

    position = len(entities.MAIN_MENU) + entities.HILIGHTED_EFFECT
    entities.MENU_FIRST_ITEM = index_double[position - entities.HIGHLIGHT_ROW]

def get_i2c(spec, sda, scl) -> object:

    i2c = entities.I2C(id = spec['ID'], sda = sda, scl = scl, freq = spec['FREQ'])

    return i2c

def get_uart(specs:dict, tx=None, rx=None) -> object:

    id = specs['ID']
    baud = specs['BAUD_RATE']

    uart = entities.UART(id, baudrate=baud, tx=tx, rx=rx)

    return uart