'''
These are the functions called from the callbacks in controller.Machine.
'''

import entities
import model
import view
import lighting


class States:
    '''String enum seems like overkill.'''

    WELCOME = 'welcome'
    EFFECTS = 'effects'
    ANIMATED = 'animated'
    STATIC = 'static'
    EDIT = 'edit'
    PAUSED = 'paused'
    STANDBY = 'standby'


entities.MACHINE_STATE = States.WELCOME
entities.STANDBY_TOGGLE = States.WELCOME


########### MACHINE_STATE: WELCOME


def welcome_turn_left():
    entities.MACHINE_STATE = States.EFFECTS
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_effects_list()

def welcome_turn_right():
    entities.MACHINE_STATE = States.EFFECTS
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_effects_list()

def welcome_click():
    entities.MACHINE_STATE = States.EFFECTS
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_effects_list()

def welcome_toggle():
    '''Puts machine in standby.'''

    entities.CLIP = entities.STANDBY_IN_CLIP
    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_empty_list()


########### MACHINE_STATE: EFFECTS


def effects_turn_left():
    '''Scrolls the effects menu.'''

    entities.EFFECTS_MENU_FIRST_ITEM -= 1
    if entities.EFFECTS_MENU_FIRST_ITEM < 0:
        entities.EFFECTS_MENU_FIRST_ITEM = len(entities.EFFECTS_MENU) - 1

    return view.get_effects_list()

def effects_turn_right():
    '''Scrolls the effects menu.'''

    entities.EFFECTS_MENU_FIRST_ITEM += 1
    if entities.EFFECTS_MENU_FIRST_ITEM > len(entities.EFFECTS_MENU) - 1:
        entities.EFFECTS_MENU_FIRST_ITEM = 0

    return view.get_effects_list()

def effects_click():
    '''Select an effect.'''

    entities.CURRENT_EFFECT = entities.EFFECTS_MENU.get(entities.EFFECTS_HILIGHTED_EFFECT)
    entities.MACHINE_STATE = States.STATIC
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'
    if not entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.MACHINE_STATE = States.ANIMATED

    lighting.set_up_effect()
    entities.WAYPOINT_START = entities.UTIME.time()

    return view.get_status_list()

def effects_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.EFFECTS_HIGHLIGHT_ROW * hilight_height

    return hilight_row

def effects_toggle():
    '''Puts machine in standby.'''

    entities.CLIP = entities.STANDBY_IN_CLIP
    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_empty_list()


########### MACHINE_STATE: ANIMATED


def animated_click():
    '''Pause effect.'''

    entities.MDB = entities.MAIN_DISPLAY_DIM
    entities.MACHINE_STATE = States.PAUSED
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

def animated_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = States.EFFECTS
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_effects_list()

def animated_increment_waypoint():

    model.increment_waypoint()

def animated_set_next_waypoint():

    if entities.WP_DUR <= 1:
            
        entities.WAYPOINT_END = entities.UTIME.time()
        entities.WAYPOINT_RUN_TIME = entities.WAYPOINT_END - entities.WAYPOINT_START

        lighting.set_next_waypoint()

        entities.WAYPOINT_START = entities.UTIME.time()
  
def animated_toggle():
    '''Puts machine in standby.'''

    entities.CLIP = entities.STANDBY_IN_CLIP
    entities.STANDBY_TOGGLE = States.ANIMATED
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_empty_list()

def animated_play_sound():
    '''Sound FX clips play in this state.'''

def animated_run_vfx():
    '''Visual effects run in this state.'''

def animated_first_line():
    '''The first line of the status screen is the time or waypoint name.'''
    '''Can't import datetime for some reason.'''

    line_format = f'^{entities.MAIN_DISPLAY_LENGTH}s' # Center on screen
    text = f'   WP: {entities.WP_NAME}'

    if entities.HOUR:

        if int(entities.HOUR) >= 24:
            entities.HOUR = 0

        hour = f'0{int(entities.HOUR)}'[-2:]
        minute = f'0{int((entities.HOUR - int(entities.HOUR))*60.0)}'[-2:]

        text = f' Hour: {hour}:{minute}'

    # return f'{text:{line_format}}'
    return text

########### MACHINE_STATE: STATIC


def static_turn_left():
    '''Scroll a color to edit.'''

    row = entities.STATIC_SELECT_ROW + 1
    entities.STATIC_SELECT_ROW = min(row, 5)

    return view.get_status_list()

def static_turn_right():
    '''Scroll a color to edit.'''

    row = entities.STATIC_SELECT_ROW - 1
    entities.STATIC_SELECT_ROW = max(1, row)

    return view.get_status_list()

def static_click():
    '''Select a color to edit.'''

    entities.MACHINE_STATE = States.EDIT
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_status_list()

def static_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = States.EFFECTS
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_effects_list()

def static_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row

def static_toggle():
    '''Puts machine in standby.'''

    entities.CLIP = entities.STANDBY_IN_CLIP
    entities.STANDBY_TOGGLE = States.STATIC
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_empty_list()

def static_bank(name, index):
    '''Toggles the named LED bank on or off.'''

    relay = f'{name}_R'

    entities.PIN(entities.PICO_PIN[relay]).toggle()
    entities.SINGLES[name][index] = entities.PIN(entities.PICO_PIN[relay]).value()

def static_play_sound():
    '''Sound FX clips play in this state.'''

def static_first_line():
    '''The first line of the status screen is the waypoint name.'''

    name = entities.CURRENT_EFFECT[0]
    line_format = f'^{entities.MAIN_DISPLAY_LENGTH}s' # Center on screen

    return f'{name:{line_format}}'


########### MACHINE_STATE: EDIT


def edit_turn_left():
    '''Reduce the selected colors brightness.'''

    index = entities.CURRENT_EFFECT[2]
    color = entities.EDIT_SCREEN_ITEMS[entities.STATIC_SELECT_ROW]

    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value -= entities.EDIT_PWM_TICKS # PWM expression
    pwm_color_value = max(pwm_color_value, 0) # PWM expression
    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>

    pwm_color_value = model.pwm_percent(pwm_color_value)
    entities.WORKING_BUFFER[color][index] = pwm_color_value # writes the new value into the STATIC_BUFFER
    lighting.set_pwm_values()

    return view.get_status_list()

def edit_turn_right():
    '''Increase the selected colors brightness.'''
    
    index = entities.CURRENT_EFFECT[2]
    color = entities.EDIT_SCREEN_ITEMS[entities.STATIC_SELECT_ROW]

    pwm_color_value = getattr(entities, color) # PWM expression
    pwm_color_value += entities.EDIT_PWM_TICKS # PWM expression
    pwm_color_value = min(pwm_color_value, entities.PWM_STEPS) # PWM expression
    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    
    pwm_color_value = model.pwm_percent(pwm_color_value)
    entities.WORKING_BUFFER[color][index] = pwm_color_value # writes the new value into the STATIC_BUFFER
    lighting.set_pwm_values()

    return view.get_status_list()

def edit_click():
    '''Return to the static menu.'''

    entities.MACHINE_STATE = States.STATIC
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_status_list()

def edit_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row

def edit_toggle():
    '''Puts machine in standby.'''

    entities.CLIP = entities.STANDBY_IN_CLIP
    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_empty_list()

def edit_bank(name, index):
    '''Toggles the named LED bank on or off.'''

    relay = f'{name}_R'

    entities.PIN(entities.PICO_PIN[relay]).toggle()
    entities.SINGLES[name][index] = entities.PIN(entities.PICO_PIN[relay]).value()

def edit_play_sound():
    '''Sound FX clips play in this state.'''

def edit_first_line():
    '''The first line of the status screen is the waypoint name.'''

    name = entities.CURRENT_EFFECT[0]
    line_format = f'^{entities.MAIN_DISPLAY_LENGTH}s' # Center on screen

    return f'{name:{line_format}}'


########### MACHINE_STATE: PAUSED


def paused_click():
    '''Unpause animated effect.'''

    entities.MACHINE_STATE = States.ANIMATED
    entities.MDB = entities.MAIN_DISPLAY_BRIGHT
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    return view.get_status_list()


########### MACHINE_STATE: STANDBY


def standby_toggle():
    '''Takes the machine out of standby.'''

    entities.CLIP = entities.STANDBY_OUT_CLIP
    entities.MACHINE_STATE = entities.STANDBY_TOGGLE
    lighting.set_bank_relays()
    entities.PROGRESS_MESSAGE = f'Machine State: {entities.MACHINE_STATE}'

    if entities.MACHINE_STATE == 'effects':
        return view.get_effects_list()

    else:
         return view.get_status_list()
