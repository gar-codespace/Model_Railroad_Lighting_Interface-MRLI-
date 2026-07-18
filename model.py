import entities
import handlers

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

def set_button_pins():
    '''
    The button library sets up the buttons.
    '''

    entities.Button(entities.PICO_PIN['BANK0_B'], "Bank0", handler=handlers.Bank0Handler())
    entities.Button(entities.PICO_PIN['BANK1_B'], "Bank1", handler=handlers.Bank1Handler())
    entities.Button(entities.PICO_PIN['BANK2_B'], "Bank2", handler=handlers.Bank2Handler())
    entities.Button(entities.PICO_PIN['BANK3_B'], "Bank2", handler=handlers.Bank2Handler())
    entities.Button(entities.PICO_PIN['BANK4_B'], "Bank2", handler=handlers.Bank2Handler())
    entities.Button(entities.PICO_PIN['SCENIC_B'], "Scenic", handler=handlers.Bank2Handler())

def get_menu_index():
    
    index_list = tuple(range(0, len(entities.ROUTINES)))
    index_list = index_list + index_list
    
    index_list = index_list[entities.SCROLL_ROUTINE:]

    return index_list

def increment_current_routine(direction:str):

    wrap = len(entities.ROUTINES) - 1

    if direction == 'right':
        entities.SCROLL_ROUTINE += 1
    elif direction == 'left':
        entities.SCROLL_ROUTINE -= 1

    if entities.SCROLL_ROUTINE < 0:
        entities.SCROLL_ROUTINE = wrap
    elif entities.SCROLL_ROUTINE > wrap:
        entities.SCROLL_ROUTINE = 0


def get_highlighted_routine(): # list comprehension
    
    x = entities.SCROLL_ROUTINE + entities.HIGHLIGHT_ROW

    if x == len(entities.ROUTINES):
        x = 0
    elif x == len(entities.ROUTINES) + 1:
        x = 1


    entities.SELECTED_ROUTINE = x
    