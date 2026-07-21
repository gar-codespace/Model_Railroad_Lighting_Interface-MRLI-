import entities
import listeners

def scenic_lights():
     # the lights that decorate the model railroad
    entities.PIN(entities.PICO_PIN['SCENIC'], entities.PIN.OUT).value(0)

def pwm2percent(pwm):
    '''
    Convert a pwm valut to percentage rounded to 3 places.
    '''

    x = pwm / entities.PWM_STEPS
    x = round(x * 100, 3)
    return x

def set_encoder_pins():
        
    entities.PIN(entities.PICO_PIN['TRA'], entities.PIN.IN, entities.PIN.PULL_UP) # Try these w/o pull up
    entities.PIN(entities.PICO_PIN['TRB'], entities.PIN.IN, entities.PIN.PULL_UP)
    entities.PIN(entities.PICO_PIN['PSH'], entities.PIN.IN, entities.PIN.PULL_UP)

def set_switch_pins():

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
    
    index_list = index_list[entities.SCROLL_EFFECTS:]

    return index_list

def increment_current_effect(direction:str):

    wrap = len(entities.EFFECTS) - 1

    if direction == 'right':
        entities.SCROLL_EFFECTS += 1
    elif direction == 'left':
        entities.SCROLL_EFFECTS -= 1

    if entities.SCROLL_EFFECTS < 0:
        entities.SCROLL_EFFECTS = wrap
    elif entities.SCROLL_EFFECTS > wrap:
        entities.SCROLL_EFFECTS = 0

def get_highlighted_effect(): # list comprehension
    
    x = entities.SCROLL_EFFECTS + entities.HIGHLIGHT_ROW

    if x == len(entities.EFFECTS):
        x = 0
    elif x == len(entities.EFFECTS) + 1:
        x = 1

    entities.SELECTED_EFFECTS = x
    
def reset_clocks():

    entities.RED_CLOCK = 0
    entities.GREEN_CLOCK = 0
    entities.BLUE_CLOCK = 0
    entities.WARM_CLOCK = 0
    entities.COOL_CLOCK = 0