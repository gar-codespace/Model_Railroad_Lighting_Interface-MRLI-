import entities


def pwm2percent(pwm):
    '''
    Convert a pwm value to decimal percentage rounded to 3 places.
    '''

    x = pwm / entities.PWM_STEPS
    y = round(x * 100, 3) # percentage
    x = round(x, 3) # decimal percentage
    return x

def set_switch_pins():
    '''
    The STEMMA relay from Adafruit that turns the led banks or scenic lighting on or off.
    '''

    entities.PIN(entities.PICO_PIN['BANK_0_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_1_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_2_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_3_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK_4_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['SCENIC_S'], entities.PIN.OUT)

def set_pwm_led_pins():
    '''
    Initializes the PWM pins.
    '''

    entities.PWM(entities.PIN(entities.PICO_PIN['RED']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['WARM']), freq=entities.PWM_FREQ)
    entities.PWM(entities.PIN(entities.PICO_PIN['COOL']), freq=entities.PWM_FREQ)
    
def get_index_double():
    '''
    IE [0, 1, 2, 3, 4, 0, 1, 2, 3 , 4]
    '''
    
    index_double = tuple(range(0, len(entities.MAIN_MENU)))
    index_double = index_double + index_double

    return index_double

def get_waypoint_duration(index):
    '''
    The duration of the waypoint is the number of times the while loop is run.
    When tested, the Picos clock was consistantly way off from real time,
    so the CLOCK_OFFSET adjusts for that.
    '''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.WP_DUR = 1
    else: # Convert duration to milliseconds
        duration = entities.ANIMATED_BUFFER['TIME'][index] # real time minutes
        duration *= 60 # real time seconds
        duration *= 1000 # real time milliseconds

        # Adjustment for asyncio overhead
        duration *= entities.CLOCK_OFFSET 

        # Apply the random factor
        random = entities.ANIMATED_BUFFER['RANDOM'][index]
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
        if next_index == len(entities.ANIMATED_BUFFER['TIME']):
            next_index = 0

        entities.NEXT_WP = int(next_index)

def get_color_delta(index:int, color:str):
    '''
    The value each color changes between waypoints expressed im PWM steps.
    Can return zero, a positive or negative value.
    '''

    if entities.CURRENT_EFFECT[1] == 'STATIC':
       color_delta = 0

    else:
        color_begin = entities.ANIMATED_BUFFER[color][index] # decimal percent
        color_end = entities.ANIMATED_BUFFER[color][entities.NEXT_WP] # decimal percent
        color_delta = color_begin - color_end # decimal percent
        color_delta = color_delta * entities.PWM_STEPS # pwm steps

    return int(color_delta)

    
