import entities


def pwm2percent(pwm):
    '''
    Convert a pwm value to percentage rounded to 3 places.
    '''

    x = pwm / entities.PWM_STEPS
    x = round(x * 100, 3)
    return x

def set_switch_pins():
    '''
    The STEMMA relay from Adafruit that turns the led banks or scenic lighting on or off.
    '''

    entities.PIN(entities.PICO_PIN['BANK0_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK1_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK2_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK3_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK4_S'], entities.PIN.OUT)
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

######## OBSOLETE ########

def adjust_color_value(direction: str):
    '''
    This method is called when the colors are manually being adjusted.
    '''

    color_being_adjusted = entities.LED_INDEX_MAP[entities.STATUS_HILIGHT_INDEX]
    pwm_color_value = entities.PWM_VALUES[color_being_adjusted]

    if direction == 'right': # turn it up
        pwm_color_value += entities.PWM_TICKS
        pwm_color_value = min(pwm_color_value, entities.PWM_STEPS)
        entities.PWM_VALUES[color_being_adjusted] = pwm_color_value

    if direction == 'left': # turn it down
        pwm_color_value -= entities.PWM_TICKS
        pwm_color_value = max(0, pwm_color_value)
        entities.PWM_VALUES[color_being_adjusted] = pwm_color_value


    x = entities.PWM(entities.PIN(entities.PICO_PIN[color_being_adjusted])).duty_u16(int(pwm_color_value))

  