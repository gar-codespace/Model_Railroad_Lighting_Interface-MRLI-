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

def set_switche_pins():

    entities.PIN(entities.PICO_PIN['BANK0'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK1'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['BANK2'], entities.PIN.OUT)
    entities.PIN(entities.PICO_PIN['SCENIC'], entities.PIN.OUT)

def set_pwm_led_pins():
        
    entities.PWM(entities.PIN(entities.PICO_PIN['RED']))
    entities.PWM(entities.PIN(entities.PICO_PIN['GREEN']))
    entities.PWM(entities.PIN(entities.PICO_PIN['BLUE']))
    entities.PWM(entities.PIN(entities.PICO_PIN['WARM']))
    entities.PWM(entities.PIN(entities.PICO_PIN['WHITE']))

def set_button_pins():

    entities.Button(entities.PICO_PIN['BACK'], "Back", handler=handlers.BackHandler())
    entities.Button(entities.PICO_PIN['BANK0_B'], "Bank0", handler=handlers.Bank0Handler())
    entities.Button(entities.PICO_PIN['BANK1_B'], "Bank1", handler=handlers.Bank1Handler())
    entities.Button(entities.PICO_PIN['BANK2_B'], "Bank2", handler=handlers.Bank2Handler())