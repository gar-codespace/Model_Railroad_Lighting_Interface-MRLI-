'''
The machine operates in one of seven ststes:
WELCOME, EFFECTS, ANIMATED, STATIC, EDIT, PAUSED, STANDBY
'''

import entities
import model
import view
import lighting


########### MACHINE_STATE: WELCOME


def WELCOME_turn_left():
    entities.MACHINE_STATE = 'EFFECTS'

    return view.get_menu_list()

def WELCOME_turn_right():
    entities.MACHINE_STATE = 'EFFECTS'

    return view.get_menu_list()

def WELCOME_click():
    entities.MACHINE_STATE = 'EFFECTS'

    return view.get_menu_list()

def WELCOME_get_hilight():
    # Move the hilight rectangle off the screen

    return 65

def WELCOME_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = 'EFFECTS'
    entities.MACHINE_STATE = 'STANDBY'
    lighting.shut_off_leds()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: EFFECTS


def EFFECTS_turn_left():
    '''Scrolls the effects menu.'''

    entities.MENU_FIRST_ITEM -= 1
    if entities.MENU_FIRST_ITEM < 0:
        entities.MENU_FIRST_ITEM = len(entities.MAIN_MENU) - 1

    return view.get_menu_list()

def EFFECTS_turn_right():
    '''Scrolls the effects menu.'''

    entities.MENU_FIRST_ITEM += 1
    if entities.MENU_FIRST_ITEM > len(entities.MAIN_MENU) - 1:
        entities.MENU_FIRST_ITEM = 0

    return view.get_menu_list()

def EFFECTS_click():
    '''Select an effect.'''

    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.MACHINE_STATE = 'STATIC'
    if not entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.MACHINE_STATE = 'ANIMATED'

    lighting.set_up_effect()
    entities.START_TIME = entities.UTIME.time()

    return view.get_status_list()

def EFFECTS_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT'] - 1
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height

    return hilight_row + 1

def EFFECTS_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = 'EFFECTS'
    entities.MACHINE_STATE = 'STANDBY'
    lighting.shut_off_leds()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: ANIMATED


def ANIMATED_click():
    '''Pause effect.'''

    entities.MACHINE_STATE = 'PAUSED'
    entities.MAIN_DISPLAY_BRIGHTNESS = entities.MAIN_DISPLAY_DIM

    print(entities.MACHINE_STATE)

    return view.get_status_list()

def ANIMATED_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = 'EFFECTS'

    return view.get_menu_list()

def ANIMATED_increment_waypoint():

    entities.RED -= entities.STEP_R
    entities.GREEN -= entities.STEP_G
    entities.BLUE -= entities.STEP_B
    entities.WARM -= entities.STEP_W
    entities.COOL -= entities.STEP_C

    entities.WP_DUR -= 1

def ANIMATED_set_next_waypoint():

    if entities.WP_DUR <= 1:
            
        entities.END_TIME = entities.UTIME.time()
        measured_time = entities.END_TIME - entities.START_TIME
        print(f'Measured duration: {measured_time} seconds')

        lighting.set_next_waypoint()

        entities.START_TIME = entities.UTIME.time()
  
def ANIMATED_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = 'ANIMATED'
    entities.MACHINE_STATE = 'STANDBY'
    lighting.shut_off_leds()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: STATIC


def STATIC_turn_left():
    '''Scroll a color to edit.'''

    row = entities.STATIC_SELECT_ROW + 1
    entities.STATIC_SELECT_ROW = min(row, 4)

    return view.get_status_list()

def STATIC_turn_right():
    '''Scroll a color to edit.'''

    row = entities.STATIC_SELECT_ROW - 1
    entities.STATIC_SELECT_ROW = max(0, row)

    return view.get_status_list()

def STATIC_click():
    '''Select a color to edit.'''

    entities.MACHINE_STATE = 'EDIT'

    return view.get_status_list()

def STATIC_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = 'EFFECTS'

    return view.get_menu_list()

def STATIC_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1

def STATIC_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = 'STATIC'
    entities.MACHINE_STATE = 'STANDBY'
    lighting.shut_off_leds()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: EDIT


def EDIT_turn_left():
    '''Reduce the selected colors brightness.'''

    index = entities.CURRENT_EFFECT[2]
    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]

    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value -= entities.PWM_TICKS # PWM expression
    pwm_color_value = max(pwm_color_value, 0) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.STATIC_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER

    lighting.set_led_values()

    return view.get_status_list()

def EDIT_turn_right():
    '''Increase the selected colors brightness.'''
    
    index = entities.CURRENT_EFFECT[2]
    color = entities.LED_INDEX_MAP[entities.STATIC_SELECT_ROW]
    
    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value += entities.PWM_TICKS # PWM expression
    pwm_color_value = min(pwm_color_value, entities.PWM_STEPS) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.STATIC_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER

    lighting.set_led_values()

    return view.get_status_list()

def EDIT_click():
    '''Return to the edit menu.'''

    entities.MACHINE_STATE = 'STATIC'

    return view.get_status_list()

def EDIT_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row - 1

def EDIT_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = 'EDIT'
    entities.MACHINE_STATE = 'STANDBY'
    lighting.shut_off_leds()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: PAUSED


def PAUSED_click():
    '''Unpause animated effect.'''

    entities.MACHINE_STATE = 'ANIMATED'
    entities.MAIN_DISPLAY_BRIGHTNESS = entities.MAIN_DISPLAY_BRIGHT
    print(entities.MACHINE_STATE)

    return view.get_status_list()


########### MACHINE_STATE: STANDBY


def STANDBY_toggle():
    '''Takes the machine out of standby.'''

    entities.MACHINE_STATE = entities.STANDBY_TOGGLE
    lighting.set_led_banks()
    # Turn on SFX
    
    return view.get_menu_list()
