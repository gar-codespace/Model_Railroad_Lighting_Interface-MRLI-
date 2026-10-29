'''
All the settings for the program are here.
All the imports are in one place.
'''

# packaged libraries are kept to a minimum
from machine import Pin as PIN, I2C, Timer as TIMER, PWM, UART
from micropython import const as CONST
from random import randint as RANDINT
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as UASYNCIO

# hardware libraries (3rd party)
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
# from hw_irq_button import IrqButton
from hw_polling_button import Button

###### PICK A DISPLAY DRIVER ######
DISPLAY_DRIVER0 = __import__('hw_sh1106').Driver_I2C # Big OLED
# DISPLAY_DRIVER1 = __import__('hw_ssd1306').Driver_I2C # Small OLED

SOUND_DRIVER0 = __import__('hw_adafruit_audio_fx').SoundFX

################## HARDWARE ######################

################## RASPI PICO PARAMETERS ######################

LED = PIN('LED', PIN.OUT)
PWM_FREQ = 480
PWM_STEPS = 65535

################## RASPI PICO PIN ASSIGNMENTS ######################

PICO_PIN = {
        'RED':26, # pwm colors
        'GREEN':27,
        'BLUE':28,
        'WARM':3,
        'COOL':4,

        'SCENIC_R':5, # relays
        'BANK_4_R':6,
        'BANK_3_R':7,
        'BANK_2_R':8,
        'BANK_1_R':9,
        'BANK_0_R':10,

        'SCENIC_B':11, # buttons
        'BANK_4_B':12,
        'BANK_3_B':13,
        'BANK_2_B':14,
        'BANK_1_B':15,
        'BANK_0_B':16,
        'CONFIRM' :22, # encoder
        
        'PSH':17, # encoder
        'TRA':18, # encoder
        'TRB':19, # encoder

        'COM0':20, # I2C SDA
        'COM1':21, # I2C SCL
        'COM2':0, # UART TX
      #   'COM3':1,
      #   'RESET':2,

        'AVAILABLE':1,
        'AVAILABLE':2,
        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        }

################## SERIAL COMMUNICATION PROTOCOLS ######################

I2C0 = {
          'TYPE':'i2c',
          'ID':0,
          'SDA':'COM0',
          'SCL':'COM1',
          'FREQ':400000
        }

UART0 = {
          'TYPE':'uart',
          'ID':0,
          'TX':'COM2',
          'RX':None,
          'FREQ':9600
        }

################## DISPLAY ######################

OLED0 = { # Main Display
        'BOARD':'Integrated display module',
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        }

MAIN_DISPLAY0 = { # Big OLED
            'BUS':'I2C0',
            'PARAMS':'OLED0',
            'DRIVER':'DISPLAY_DRIVER0'
            }
MAIN_DISPLAY1 = { # Small OLED
            'BUS':'I2C0',
            'PARAMS':'OLED0',
            'DRIVER':'DISPLAY_DRIVER1'
            }

DISPLAY_BRIGHT = 70
DISPLAY_DIM = 1

MAIN_DISPLAY_BRIGHT = DISPLAY_BRIGHT
MAIN_FORMAT =  {
                'LINE_HEIGHT': 10, # Pixels
                'ROWS': 6,
                'CHAR_PER_ROW':15,
                'X_OFFSET': 4, # Pixels
                }

################## SOUND ######################

SB0 = {
       'BOARD': 'Adafruit Sound FX Board',
       'WAIT':50,
       'DUPLEX':False,
       'RESET':False,
       }

SOUND_CARD0 = {
            'BUS':'UART0',
            'PARAMS':'SB0',
            'DRIVER':'SOUND_DRIVER0'
            }

################## PUSH BUTTON PARAMETERS ######################

BUTTON0 = {
            'NORMALLY_OPEN':True, # False for NORMALLY_CLOSED
            'DEBOUNCE_TIME':50,
            'MULTI_TIME':200,
            'PRESSED_MSG':'button pressed',
            'RELEASED_MSG':'button released',
            'MULTI_MSG':'multiple presses',
            }

################## SOFTWARE ######################

################## TIME BASE ######################

FAST_TIME_CLOCK = 8 # used in model railroading to compress time.
DEFAULT_CYCLE = 20 # milliseconds used for other awaits
WAYPOINT_START = 0 # Used for the waypoint duration measurement.
WAYPOINT_END = 0 # Used for the waypoint duration measurement.
WAYPOINT_RUN_TIME = 0 # Time the waypoint actually ran (sec)

################## NAVIGATION ######################

MACHINE_STATE:str  = None
STANDBY_TOGGLE:str = None
PROGRESS_MESSAGE:str = f'Model Railroad Lighting Automation v20261001.1.1'

STARTUP_EFFECT_DURATION = 5000 # Milliseconds
WELCOME_SCREEN = ['M.U.T.T.', 'Metropolitan', 'Union ', 'Transfer', 'Terminal'] # 6 lines maximum, 15 char per line

EFFECTS_MENU = { #     Name             Type    Index
             0: ('Maintenance',   'STATIC',  1),
             1: ('Daytime',       'STATIC',  2),
             2: ('Overcast',      'STATIC',  3),
             3: ('Twilight',      'STATIC',  5),
             4: ('Nightime',      'STATIC',  4),
             5: ('11PM',         'ALL_DAY',  0),
             6: ('3AM',          'ALL_DAY',  2),
             7: ('7AM',          'ALL_DAY',  4),
             8: ('11AM',         'ALL_DAY',  6),
             9: ('3PM',          'ALL_DAY',  8),
            10: ('7PM',          'ALL_DAY', 10),
            11: ('A Cloudy Day',  'CLOUDY',  0),
            12: ('Stormy Night',  'STORMY',  0)
            } # In the order they show on the display
EFFECTS_HIGHLIGHT_ROW = 2 # which row is hilighted
EFFECTS_HILIGHTED_EFFECT = 1 # EFFECTS_MENU key and default effect
EFFECTS_MENU_FIRST_ITEM:int # calculated on startup by model.get_menu_first_item()
EFFECTS_MENU_STATIC_SYMBOL = '|'
EFFECTS_MENU_ANIMATED_SYMBOL = '>'
CURRENT_EFFECT = EFFECTS_MENU[EFFECTS_HILIGHTED_EFFECT] # Must be a STATIC effect. Also used as the default effect.

STATIC_SELECT_ROW = 3 # In STATIC state, the encoder moves the rectangle up and down

EDIT_ROUNDING_VALUE = 4
EDIT_SCREEN_ITEMS = [
                 'WP_NAME',
                 'RED',
                 'GREEN',
                 'BLUE',
                 'WARM',
                 'COOL'
                ]
EDIT_PWM_TICKS = 10 # How many ticks per indent of the rotary encoder when changing color values.
                # Smaller is finer control.

################## BUFFERS ######################

WORKING_BUFFER = {} # Either the static dictionary or one of the animated dictionaries is copied into this.

################## EFFECT BUFFER ######################
# The running effect writes to and reads from this buffer.
# In STATIC state user inputs are written here.
# The slower the clock cycle, the more accurate the delay.
CLOCK_CYCLE = 500 # Milliseconds. WP_DUR * CLOCK_CYCLE = total time of the waypoint
CLOCK_OFFSET = 1 # Adjusts for asyncio overhead slowing down the effects. Smaller = faster.
                 
RED     :int = 32500 # PWM value
GREEN   :int = 32500
BLUE    :int = 32500
WARM    :int = 32500
COOL    :int = 32500
BANK_0  :int = 1 # 1 is on, 0 is off
BANK_1  :int = 1
BANK_2  :int = 1
BANK_3  :int = 1
BANK_4  :int = 1
SCENIC  :int = 1
CUR_WP  :int = None
WP_DUR  :int = 1 # waypoint_duration is the number of times the effect will await, given a delay of entities.CLOCK_CYCLE
NEXT_WP :int = 0 # Index of the next waypoint
WP_NAME :str = 'name'
HOUR  :float = 0.0 # Fast time clock display
TIME    :int = 0
CLIP  :tuple = None # sound clip
CLIP_G  :str = None # the name of the group, not the members
STEP_R  :int = 0 # how much in pwm steps does each color change per CLOCK_CYCLE. pos or neg
STEP_G  :int = 0
STEP_B  :int = 0
STEP_W  :int = 0
STEP_C  :int = 0
STEP_H:float = 0.0 # Increment the hour
################## EFFECT BUFFER ######################


################## LIGHTING EFFECT DEFINITIONS ######################

'''
In the dictionary for each effect, the duration of the effect is given in real time minutes,
the time the effect actually takes in the real world.
The duration is then adjusted for model railroad 'scale' and converted to milliseconds.

SINGLES effects have one waypoint. The duration is defined as 0, since 'infinately long' seems rediculous.
The random value is a float between 0 and 1. 0 is not random, 1 is maximum randomness.
'''

SINGLES = {
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stby', 'Maint',   'Day',   'Ovcst', 'Night', 'Twili'), # Waypoint name
'GROUP':  (   'A1',    'A1',    'A3',      'A3',    'A5',    'A4'), # sound effects group
'HOUR':   (      0,       0,       0,         0,       0,       0),
'TIME':   (      0,       0,       0,         0,       0,       0), # duration of waypoint
'RANDOM': (     .0,      .0,      .0,        .0,      .0,      .0),
'RED':    [      0,       0,       0,         0,       0,    .004],
'GREEN':  [      0,       0,       0,         0,       0,    .006],
'BLUE':   [      0,       0,       0,         0,   .0035,       0],
'WARM':   [      0,     .99,     .22,      .002,       0,    .005],
'COOL':   [      0,     .99,     .02,      .002,   .0008,       0],
'BANK_0': [      1,       1,       1,         1,       0,      0,],
'BANK_1': [      0,       1,       0,         0,       0,      0,],
'BANK_2': [      0,       1,       1,         0,       0,      0,],
'BANK_3': [      0,       0,       1,         0,       0,      0,],
'BANK_4': [      0,       1,       1,         1,       1,      1,],
'SCENIC': [      0,       1,       0,         1,       1,      1,],
}

################## ANIMATED LIGHTING EFFECTS ######################

# Each column of an animated effect is being called a waypoint
ALL_DAY = { # simulates an entire day
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : .860,
'NAME':   ( '23:00', '01:00', '03:00', '05:00', '07:00', '09:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00'), # Waypoint name
'GROUP':  (    'A5',    'A5',    'A5',    'A4',    'A3',    'A3',    'A3',    'A3',    'A3',    'A4',    'A4',    'A5'), # sound effects group
'HOUR':   (      23,       1,       3,       5,       7,       9,      11,      13,      15,      17,      19,      21), # the time of day
'TIME':   (     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120), # duration of waypoint in real time minutes
'RANDOM': (      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0), 
'RED':    [    0.00,    0.00,    0.00,    .000,    .004,    0.02,    0.00,    0.00,    0.00,    .003,    .006,    .003],
'GREEN':  [    0.00,    0.00,    0.00,    0.00,    .006,    0.02,    0.00,    0.00,    0.00,    .002,    .004,    .002],
'BLUE':   [    .001,   .0005,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00],
'WARM':   [    0.00,    0.00,    0.00,    .000,    .005,    0.12,    0.18,    0.18,    0.22,    0.10,    .005,    .003],
'COOL':   [    .001,    .001,    .001,    0.00,    0.00,    0.01,    0.02,    0.03,    0.02,    .001,    0.00,    .000],
'BANK_0': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_1': [       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0],
'BANK_2': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_3': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_4': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'SCENIC': [       1,       1,       1,       1,       1,       0,       0,       0,       0,       1,       1,       1],
}

STORMY = { # Simulates a stormy night
'CLOCK_CYCLE'  : 8,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stormy','Roll Out',  'Clear', 'Roll In'), # Waypoint name
'GROUP':  (    'D1',       'D1',     'D1',      'D1'), # sound effects group
'HOUR':   (       0,          0,        0,         0),
'TIME':   (     1.0,        1.2,      1.0,       1.2), # duration of waypoint in minutes
'RANDOM': (      .8,         .8,       .8,        .8),
'RED':    [    0.00,       0.00,     0.00,      0.00],
'GREEN':  [    0.00,       0.00,     0.00,      0.00],
'BLUE':   [   .0035,      .0035,    .0035,     .0035],
'WARM':   [    0.00,       0.00,     0.00,      0.00],
'COOL':   [    .000,       .000,    .0009,     .0009],
'BANK_0': [       0,          0,        0,         0],
'BANK_1': [       0,          0,        0,         0],
'BANK_2': [       0,          0,        0,         0],
'BANK_3': [       0,          0,        0,         0],
'BANK_4': [       1,          1,        1,         1],
'SCENIC': [       1,          1,        1,         1],
}

CLOUDY = { # Simulates a cloudy day
'CLOCK_CYCLE'  : 25,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Clear','Roll In', 'Cloudy','Roll Out'), # Waypoint name
'GROUP':  (    'A3',     'A3',     'A3',      'A3'), # sound effects group
'HOUR':   (       0,        0,        0,         0),
'TIME':   (       4,      3.5,      2.5,       3.5), # duration of waypoint in real time minutes
'RANDOM': (      .7,       .7,       .7,        .7),
'RED':    [    0.00,     0.00,     0.00,      0.00],
'GREEN':  [    0.00,     0.00,     0.00,      0.00],
'BLUE':   [    0.00,     0.00,     0.00,      0.00],
'WARM':   [     .22,      .22,     .045,      .045],
'COOL':   [     .02,      .02,     .026,      .026],
'BANK_0': [       1,        1,        1,         1],
'BANK_1': [       0,        0,        0,         0],
'BANK_2': [       1,        1,        1,         1],
'BANK_3': [       1,        1,        1,         1],
'BANK_4': [       1,        1,        1,         1],
'SCENIC': [       0,        0,        0,         0],
}

################## AMBIENT SOUND DEFINITIONS ######################

PAD_MIN = 2000 # Pad is the time between ambient sound (ms)
PAD_MAX = 20000 # maximum time between ambient sounds (ms)
WELCOME_CLIP = 'clip10'
STANDBY_IN_CLIP = 'clip23'
STANDBY_OUT_CLIP = 'clip09'
PAUSE_CLIP = None
UNPAUSE_CLIP = None
CLIP = WELCOME_CLIP

# The library of sound effects:
AMBIENCE = {  # File    Name,       Duration, Description   VFX   Vol flag
                'clip00':('SILENCE0OGG', 10, 'Silence',     None),
                'clip01':('GULLS001OGG', 16, 'Seagulls 1',  None),
                'clip02':('GULLS002OGG',  9, 'Seagulls 2',  None),
                'clip03':('GULLS003OGG',  8, 'Seagulls 3',  None),
                'clip04':('GULLS004OGG', 13, 'Seagulls 4',  None),
                'clip05':('GULLS005OGG', 20, 'Seagulls 5',  None),
                'clip06':('BELL0001OGG',  6, 'Bells 1',     None, 1),
                'clip07':('BELL0002OGG',  5, 'Bells 2',     None, 1),
                'clip08':('BELL0003OGG',  3, 'Bells 3',     None, 1),
                'clip09':('WHISTLE1OGG',  3, 'Whistle 1',   None, 1),
                'clip10':('WELCOME1OGG',  6, 'Welcome',     None),
                'clip11':('BRODY001OGG',  2, 'Brody 1',     None, 1),
                'clip12':('TRAIN001OGG', 12, 'Train 1',     None),
                'clip13':('TRAIN002OGG', 12, 'Train 2',     None),
                'clip14':('TRAIN002OGG',  9, 'Train 3',     None),
                'clip15':('HORN0001OGG',  5, 'Horn 1',      None), # Not used
                'clip16':('HORN0002OGG',  5, 'Horn 2',      None),
                'clip17':('HORN0003OGG',  5, 'Horn 3',      None),
                'clip18':('CRICKET1OGG',  8, 'Cricket 1',   None),
                'clip19':('CRICKET2OGG',  7, 'Cricket 2',   None),
                'clip20':('MORNING1OGG', 12, 'Morning 1',   None),
                'clip21':('MORNING2OGG', 19, 'Morning 2',   None),
                'clip22':('NIGHT001OGG', 11, 'Night 1',     None),
                'clip23':('OWL00001OGG',  1, 'Owl 1',       None, 1),
                'clip24':('OWL00002OGG',  3, 'Owl 2',       None, 1),
                'clip25':('THUNDER0OGG',  9, 'Thunder 0',   None),
                'clip26':('THUNDER1OGG', 12, 'Thunder 1',   None),
                'clip27':('THUNDER2OGG', 18, 'Thunder 2', 'bolt'),
                'clip28':('THUNDER3OGG', 11, 'Thunder 3', 'bolt'),
                'clip29':('THUNDER4OGG', 19, 'Thunder 4', 'bolt'),
                'clip30':('WIND0001OGG', 19, 'Wind 1',      None),
                'clip31':('WIND0002OGG', 19, 'Wind 2',      None),
                'clip32':('BELLS004OGG',  7, 'Bells 4',     None,1),
                'clip33':('BELLS005OGG',  7, 'Bells 5',     None,1),
                'clip34':('BELLS006OGG',  6, 'Bells 6',     None,1),
                'clip35':('HORN0004OGG',  5, 'Horn 4',      None,1),
                'clip36':('HORN0005OGG',  5, 'Horn 5',      None,1),
                'clip37':('GEESE001OGG',  7, 'Geese 1',     None),
                'clip38':('GEESE002OGG',  7, 'Geese 2',     None),
                'clip39':('GULLS006OGG',  8, 'Seagulls 6',  None), # Same as Seagulls 1
               } # The name is conformed to the soundboard specification

# SFX Groups
A1 = [ # silence
      'clip00'
      ]

A3 = [ # Daytime
      'clip01', # Seagulls
      'clip02', # Seagulls
      'clip03', # Seagulls
      'clip04', # Seagulls
      'clip05', # Seagulls
      'clip06', # Bells
      'clip07', # Bells
      'clip08', # Bells
      'clip09', # Whistle
      'clip11', # Brody 
      'clip12', # Train 
      'clip13', # Train 
      'clip14', # Train 
      'clip39', # Seagulls
      'clip16', # Horn
      'clip17', # Horn
      'clip35', # Horn
      'clip36', # Horn
      ]

A4 = [ # Twlight, same as day + crickets + morning + geese - gulls
      'clip06', # Bells
      'clip07', # Bells
      'clip08', # Bells
      'clip09', # Whistle
      'clip11', # Brody 
      'clip12', # Train 
      'clip13', # Train 
      'clip14', # Train 
      'clip39', # Seagulls
      'clip16', # Horn
      'clip17', # Horn
      'clip18', # Cricket
      'clip19', # Cricket
      'clip20', # Morning
      'clip21', # Morning
      'clip35', # Horn
      'clip36', # Horn
      'clip37', # Geese
      'clip38'  # Geese
      ]

A5 = [ # Night time, daytime - gulls + crickets + owles
      'clip06', # Bell
      'clip07', # Bell
      'clip08', # Bell
      'clip09', # Whistle
      'clip11', # Brody
      'clip12', # Train
      'clip13', # Train
      'clip14', # Train
      'clip16', # Horn
      'clip17', # Horn
      'clip18', # Cricket
      'clip19', # Cricket
      'clip19', # Cricket
      'clip22', # Night
      'clip23', # Owl
      'clip24', # Owl
      'clip36', # Horn
      ]

D11 = [ # Stormy
      'clip27', # Thunder
      'clip27', # Thunder
      'clip28', # Thunder
      'clip28', # Thunder
      'clip29', # Thunder
      'clip30', # Wind
      'clip31', # Wind
      'clip31', # Wind
      'clip32', # Bells 
      'clip33', # Bells 
      'clip12', # Train
      'clip13', # Train
      'clip14', # Train
      'clip11', # Brody
      'clip35', # Horn
      'clip36', # Horn
      ]

D1 = [ # Stormy test
      'clip27',
      'clip28',
      'clip29',
      ]

################## VISUAL EFFECTS ######################

LIGHTNING = [# pwm, MS
             (1400, 40),
             (1000, 40),
             (800, 40),
             (600, 40),
             (400, 40),
             (1400, 80),
             (1000, 80),
             (800, 80),
             (600, 80),
             (400, 80),
             (1000, 80),
             (600, 80),
             (200, 80),
             (0, 40),
             (0, 80),
             (0, 120),
             (0, 160),
             (0, 240),
             (0, 280)
             ]
