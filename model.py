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
    '''

    duration = entities.ANIMATED_BUFFER['TIME'][index] # real time minutes
    duration = duration * 60 # real time seconds
    random = 1 - entities.ANIMATED_BUFFER['RANDOM'][index]
    xmax = duration # seconds
    xmin = duration * random # seconds
    duration = entities.RANDOM.randint(int(xmin), int(xmax)) # seconds
    duration = duration * 1000 # adjusted duration in milliseconds
    waypoint_duration = int(duration / entities.CLOCK_CYCLE)

    return waypoint_duration