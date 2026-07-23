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
    The physical switch that turns the led banks or scenic lighting on or off.
    '''

    entities.PIN(entities.PICO_PIN['BANK0_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK1_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK2_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK3_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK4_S'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['SCENIC_S'], entities.PIN.OUT)

def set_pwm_led_pins():
        
    entities.PWM(entities.PIN(entities.PICO_PIN['RED']))
    entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']))
    entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']))
    entities.PWM(entities.PIN(entities.PICO_PIN['WARM']))
    entities.PWM(entities.PIN(entities.PICO_PIN['COOL']))

def get_menu_index():
    
    index_list = tuple(range(0, len(entities.EFFECTS)))
    index_list = index_list + index_list
    
    index_list = index_list[entities.SCROLL_EFFECT:]

    return index_list

def increment_current_effect(direction:str):

    wrap = len(entities.EFFECTS) - 1

    if direction == 'right':
        entities.SCROLL_EFFECT += 1
    elif direction == 'left':
        entities.SCROLL_EFFECT -= 1

    if entities.SCROLL_EFFECT < 0:
        entities.SCROLL_EFFECT = wrap
    elif entities.SCROLL_EFFECT > wrap:
        entities.SCROLL_EFFECT = 0

def get_highlighted_effect(): # list comprehension
    
    x = entities.SCROLL_EFFECT + entities.HIGHLIGHT_ROW

    if x == len(entities.EFFECTS):
        x = 0
    elif x == len(entities.EFFECTS) + 1:
        x = 1

    entities.SELECTED_EFFECT = x
    
def reset_clocks():

    entities.RED_CLOCK = 0
    entities.GREEN_CLOCK = 0
    entities.BLUE_CLOCK = 0
    entities.WARM_CLOCK = 0
    entities.COOL_CLOCK = 0

def adjust_color_value(direction: str): # move to model?
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


    entities.PWM(entities.PIN(entities.PICO_PIN[color_being_adjusted])).duty_u16(int(pwm_color_value))

  