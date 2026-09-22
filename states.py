import entities
import model
import view
import lighting


class States:

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

    return view.get_menu_list()

def welcome_turn_right():
    entities.MACHINE_STATE = States.EFFECTS

    return view.get_menu_list()

def welcome_click():
    entities.MACHINE_STATE = States.EFFECTS

    return view.get_menu_list()

def welcome_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    # sound.stop_sfx

    return view.get_empty_list()


########### MACHINE_STATE: EFFECTS


def effects_turn_left():
    '''Scrolls the effects menu.'''

    entities.MENU_FIRST_ITEM -= 1
    if entities.MENU_FIRST_ITEM < 0:
        entities.MENU_FIRST_ITEM = len(entities.MAIN_MENU) - 1

    return view.get_menu_list()

def effects_turn_right():
    '''Scrolls the effects menu.'''

    entities.MENU_FIRST_ITEM += 1
    if entities.MENU_FIRST_ITEM > len(entities.MAIN_MENU) - 1:
        entities.MENU_FIRST_ITEM = 0

    return view.get_menu_list()

def effects_click():
    '''Select an effect.'''

    entities.CURRENT_EFFECT = entities.MAIN_MENU.get(entities.HILIGHTED_EFFECT)
    entities.MACHINE_STATE = States.STATIC
    if not entities.CURRENT_EFFECT[1] == 'STATIC':
        entities.MACHINE_STATE = States.ANIMATED

    lighting.set_up_effect()
    entities.START_TIME = entities.UTIME.time()

    return view.get_status_list()

def effects_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.HIGHLIGHT_ROW * hilight_height

    return hilight_row

def effects_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    # sound.stop_sfx

    return view.get_empty_list()

def effects_play_sound():
    '''Sound FX clips play in this state.'''


########### MACHINE_STATE: ANIMATED


def animated_click():
    '''Pause effect.'''

    entities.MACHINE_STATE = States.PAUSED
    entities.MAIN_DISPLAY_BRIGHTNESS = entities.MAIN_DISPLAY_DIM

    return view.get_status_list()

def animated_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = States.EFFECTS

    return view.get_menu_list()

def animated_increment_waypoint():

    model.increment_colors()

def animated_set_next_waypoint():

    if entities.WP_DUR <= 1:
            
        entities.END_TIME = entities.UTIME.time()
        measured_time = entities.END_TIME - entities.START_TIME
        print(f'Measured duration: {measured_time} seconds')

        lighting.set_next_waypoint()

        entities.START_TIME = entities.UTIME.time()
  
def animated_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = States.ANIMATED
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()

    return view.get_empty_list()

def animated_play_sound():
    '''Sound FX clips play in this state.'''

def animated_run_vfx(vfx:str):
    '''Runs the associated visual effect if it exists.'''

    try:
        attrib = f'run_{vfx}'
        getattr(lighting, attrib)() # IE lighting.run_bolt()

    except:
        pass


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

    return view.get_status_list()

def static_click2():
    '''Return to the effects menu.'''
    
    entities.MACHINE_STATE = States.EFFECTS

    return view.get_menu_list()

def static_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row

def static_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = States.STATIC
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    # sound.stop_sfx

    return view.get_empty_list()

def static_bank(name, index):
    '''Toggles the named LED bank on or off.'''

    relay = f'{name}_R'

    entities.PIN(entities.PICO_PIN[relay]).toggle()
    entities.SINGLES[name][index] = entities.PIN(entities.PICO_PIN[relay]).value()

def static_play_sound():
    '''Sound FX clips play in this state.'''


########### MACHINE_STATE: EDIT


def edit_turn_left():
    '''Reduce the selected colors brightness.'''

    index = entities.CURRENT_EFFECT[2]
    color = entities.EDIT_SCREEN_ITEMS[entities.STATIC_SELECT_ROW]
    pwm_color_value = getattr(entities, color) # PWM expression

    pwm_color_value -= entities.PWM_TICKS # PWM expression
    pwm_color_value = max(pwm_color_value, 0) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.WORKING_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER
    lighting.set_led_values()

    return view.get_status_list()

def edit_turn_right():
    '''Increase the selected colors brightness.'''
    
    index = entities.CURRENT_EFFECT[2]
    color = entities.EDIT_SCREEN_ITEMS[entities.STATIC_SELECT_ROW]
    pwm_color_value = getattr(entities, color) # PWM expression

    pwm_color_value += entities.PWM_TICKS # PWM expression
    pwm_color_value = min(pwm_color_value, entities.PWM_STEPS) # PWM expression

    setattr(entities, color, pwm_color_value) # writes the new value to entities.<color>
    entities.WORKING_BUFFER[color][index] = model.pwm2percent(pwm_color_value) # writes the new value into the STATIC_BUFFER
    lighting.set_led_values()

    return view.get_status_list()

def edit_click():
    '''Return to the static menu.'''

    entities.MACHINE_STATE = States.STATIC

    return view.get_status_list()

def edit_get_hilight():

    hilight_height = entities.MAIN_FORMAT['LINE_HEIGHT']
    hilight_row = entities.STATIC_SELECT_ROW * hilight_height

    return hilight_row

def edit_toggle():
    '''Puts machine in standby.'''

    entities.STANDBY_TOGGLE = States.EFFECTS
    entities.MACHINE_STATE = States.STANDBY
    lighting.shut_off_led_banks()
    # sound.stop_sfx

    return view.get_empty_list()

def edit_bank(name, index):
    '''Toggles the named LED bank on or off.'''

    relay = f'{name}_R'

    entities.PIN(entities.PICO_PIN[relay]).toggle()
    entities.SINGLES[name][index] = entities.PIN(entities.PICO_PIN[relay]).value()


def edit_play_sound():
    '''Sound FX clips play in this state.'''


########### MACHINE_STATE: PAUSED


def paused_click():
    '''Unpause animated effect.'''

    entities.MACHINE_STATE = States.ANIMATED
    entities.MAIN_DISPLAY_BRIGHTNESS = entities.MAIN_DISPLAY_BRIGHT

    return view.get_status_list()


########### MACHINE_STATE: STANDBY


def standby_toggle():
    '''Takes the machine out of standby.'''

    entities.MACHINE_STATE = entities.STANDBY_TOGGLE
    lighting.set_led_banks()
    # Turn on SFX
    
    return view.get_menu_list()
