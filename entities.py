'''
All the settings for the program are here.
Everything is upper case, even though some settings are constants and some are variables.
Oh well. That's what version 2 is for.
Also, I like to keep all the imports in one place.
'''

__version__ = '20260901.1.1'
__repo__ = 'https://github.com/gar-codespace/Diorama_Lighting_Automation'

###### PICK A DISPLAY DRIVER ######

# Choose this for the 1.3 inch display
DISPLAY_DRIVER = 'hw_sh1106'

# Choose this for the 0.9 inch display
# DISPLAY_DRIVER = 'hw_ssd1306'


# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM
from micropython import const as CONST
from random import randint as RANDINT
import os as OS
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as UASYNCIO

# hardware libraries (3rd party)
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button
DISPLAY_LIBRARY = __import__(DISPLAY_DRIVER)

SFX_PATH = f'{OS.getcwd()}/sfx'

################## HARDWARE ######################

################## RASPI PICO PARAMETERS ######################

LED = PIN('LED', PIN.OUT)
PWM_FREQ = 480
PWM_STEPS = 65535

################## RASPI PICO PIN ASSIGNMENTS ######################

PICO_PIN = {
        'RED':0, # pwm colors
        'GREEN':1,
        'BLUE':2,
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

        'SDA':20, # display
        'SCL':21, # display

        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        'Available':26,
        'Available':27,
        'Available':28 # encoder
        }

'''
There seems to be a lot of hard coding around the display having 5 lines of text.
Look into abstracting this.
'''

# OLED0 specs
OLED0 = {'ADDRESS': CONST(0x3C),
         'WIDTH': 128,
         'HEIGHT': 64,
         'LINE_HEIGHT': 14,
        }

# OLED Configurations (bus, width, height, addr)
DISPLAY0 = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])
MAIN_DISPLAY = DISPLAY0
MAIN_DISPLAY_BRIGHT = 70
MAIN_DISPLAY_DIM = 1
MAIN_DISPLAY_BRIGHTNESS = MAIN_DISPLAY_BRIGHT

# Display formatting
MAIN_FORMAT =  {'LINE_HEIGHT': 13,
                'ROWS': 5,
                'X_OFFSET': 4
                }

# Sound Hardware

SOUND_CARD = {'a':'b', 'c':'d'}


################## SOFTWARE ######################

################## TIME BASE ######################

FAST_TIME_CLOCK = 8 # used in model railroading to compress time.
DEFAULT_CYCLE = 20 # milliseconds used for other awaits
                   # Adjusts for asyncio overhead slowing down the effects.
START_TIME = 0 # Used for the waypoint duration measurement.
END_TIME = 0

################## COLOR CONTROL ######################

################## EFFECT BUFFER ######################
# The running effect writes to and reads from this buffer.
# In STATIC mode user inputs are written here and the STATIC_BUFFER.
# The slower the clock cycle, the more accurate the delay.
CLOCK_CYCLE = 500 # Milliseconds per cycle. The delay the effect awaits.
CLOCK_OFFSET = 1 # Adjustment to keep the effect times closer to what they should be.
RED     = 32500 # PWM value
BLUE    = 32500
WARM    = 32500
COOL    = 32500
BANK_0  = 1 # 1 is on, 0 is off
BANK_1  = 1
BANK_2  = 1
BANK_3  = 1
BANK_4  = 1
SCENIC  = 1
WP_DUR  = 1 # waypoint_duration is the number of times the effect will await, given a delay of entities.CLOCK_CYCLE
NEXT_WP = 0 # Index of the next waypoint
STEP_R  = 0 # how much in pwm steps does each color change per CLOCK_CYCLE. pos or neg
STEP_G  = 0
STEP_B  = 0
STEP_W  = 0
STEP_C  = 0
WP_NAME = 'name'
SFX_GRP = None
SFX_NAME= 'name'
################## EFFECT BUFFER ######################

################## NAVIGATION ######################

MACHINE_STATE = 'WELCOME' # Can be: WELCOME, EFFECTS, ANIMATED, STATIC, EDIT, PAUSED, STANDBY
STANDBY_TOGGLE = 'WELCOME'

WELCOME_SCREEN = ['   M.U.T.T.',
                  ' Metropolitan',
                  '    Union',
                  '   Transfer',
                  '   Terminal'
                  ]
HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling effects
STATIC_SELECT_ROW = 2 # In STATIC mode, the encoder moves the rectangle up and down
CURRENT_EFFECT = ('Daytime', 'STATIC', 2) # Also used as the default effect
HILIGHTED_EFFECT = 1 # MAIN_MENU key
# MENU_FIRST_ITEM is hard coded based on 5 menu lines and the highlite on line 2
# This should be abstracted
MENU_FIRST_ITEM = 12 # Index of MAIN_MENU for first item in menu
LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }
PWM_TICKS = 100 # How many ticks per indent of the rotary encoder when changing color values.
                # Smaller is finer control.

MAIN_MENU = { # In the order they show on the display
             0: ('Maintenance',        'STATIC',  1),
             1: ('Daytime',            'STATIC',  2),
             2: ('Overcast',           'STATIC',  3),
             3: ('Twilight',           'STATIC',  5),
             4: ('Nightime',           'STATIC',  4),
             5: ('* 11PM',            'ALL_DAY',  0),
             6: ('* 3AM',             'ALL_DAY',  2),
             7: ('* 7AM',             'ALL_DAY',  4),
             8: ('* 11AM',            'ALL_DAY',  6),
             9: ('* 3PM',             'ALL_DAY',  8),
            10: ('* 7PM',             'ALL_DAY', 10),
            11: ('* A Cloudy Day',     'CLOUDY',  0),
            12: ('* Stormy Night',     'STORMY',  0)
            }

################## LIGHTING EFFECT DEFINITIONS ######################

WORKING_BUFFER = {} # Either the static buffer or one of the animated buffers is copied into this.

'''
Note:
The random value is a float between 0 and 1.
0 is not random, 1 is max randomness.
'''

STATIC = {
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stby', 'Maint',   'Day',   'Fog', 'Night', 'Twili'), # Waypoint name
'GROUP':  (   'A1',    'A1',    'A3',    'A3',    'A4',    'A5'), # sound effects group
'FRAME':  (      1,       1,       1,       1,       1,       1), # Keyframe marker
'TIME':   (      0,       0,       0,       0,       0,       0), # duration of waypoint
'RANDOM': (     .0,      .0,      .0,      .0,      .0,      .0),

'RED':    [      0,       0,       0,       0,       0,      .1],
'GREEN':  [      0,       0,       0,       0,       0,      .1],
'BLUE':   [      0,       0,       0,       0,    .002,       0],
'WARM':   [      0,     .99,     .22,    .002,       0,     .05],
'COOL':   [      0,     .99,     .02,    .002,    .002,       0],

'BANK_0': [      0,       1,       1,       1,       0,      0,],
'BANK_1': [      0,       1,       0,       0,       0,      0,],
'BANK_2': [      0,       1,       1,       0,       0,      0,],
'BANK_3': [      0,       0,       1,       0,       0,      0,],
'BANK_4': [      0,       1,       1,       1,       1,      1,],
'SCENIC': [      0,       0,       0,       0,       0,      0,],
}

# Each column of an animated effect is being called a waypoint
ALL_DAY = { # simulates an entire day
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : .864,
'NAME':   ( '23:00', '01:00', '03:00', '05:00', '07:00', '09:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00'), # Waypoint name
'GROUP':  (    'B2',    'B2',    'B2',    'B1',    'B1',    'B1',    'B1',    'B1',    'B1',    'B1',    'B2',    'B2'), # sound effects group
'FRAME':  (       1,       0,       1,       0,       1,       0,       1,       0,       1,       0,       1,       0), # Keyframe marker
'TIME':   (     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120), # duration of waypoint in real time minutes
'RANDOM': (      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0), 

'RED':    [    0.00,    0.00,    0.00,    .002,    .004,    0.02,    0.00,    0.00,    0.00,    .003,    .006,    .003],
'GREEN':  [    0.00,    0.00,    0.00,    0.00,    .006,    0.02,    0.00,    0.00,    0.00,    .002,    .004,    0.00],
'BLUE':   [    .001,   .0005,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00],
'WARM':   [    0.00,    0.00,    0.00,    .001,    .005,    0.12,    0.18,    0.18,    0.22,    0.10,    .005,    0.00],
'COOL':   [    .001,    .001,    0.00,    0.00,    0.00,    0.01,    0.02,    0.03,    0.02,    .001,    0.00,    .000],

'BANK_0': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_1': [       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0],
'BANK_2': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_3': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_4': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'SCENIC': [       1,       1,       1,       1,       1,       0,       0,       0,       0,       1,       1,       1],
}

STORMY = { # Simulates a stormy night
'CLOCK_CYCLE'  : 25,
'CLOCK_OFFSET' : .4,
'NAME':   ( 'Clear','Roll In',  'STORMY','Roll Out'), # Waypoint name
'GROUP':  (    'D1',     'D1',      'D1',      'D1'), # sound effects group
'FRAME':  (       1,        1,         1,         1), # Keyframe marker
'TIME':   (       3,        2,         2,         1), # duration of waypoint in minutes
'RANDOM': (      .7,       .7,        .7,        .7),

'RED':    [    0.00,     0.00,      0.00,      0.00],
'GREEN':  [    0.00,     0.00,      0.00,      0.00],
'BLUE':   [    .001,     .001,      .000,     .0005],
'WARM':   [    0.00,     0.00,      0.00,      0.00],
'COOL':   [    .001,     .001,     .0005,      .001],

'BANK_0': [       1,        1,         1,         1],
'BANK_1': [       0,        0,         0,         0],
'BANK_2': [       0,        0,         0,         0],
'BANK_3': [       0,        0,         0,         0],
'BANK_4': [       1,        1,         1,         1],
'SCENIC': [       1,        1,         1,         1],
}

CLOUDY = { # Simulates a cloudy day
'CLOCK_CYCLE'  : 25,
'CLOCK_OFFSET' : .6,
'NAME':   ( 'Clear','Roll In', 'Cloudy','Roll Out'), # Waypoint name
'GROUP':  (    'C1',     'C1',     'C1',      'C1'), # sound effects group
'FRAME':  (       1,        1,        1,         1), # Keyframe marker
'TIME':   (       4,      2.5,      2.5,         2), # duration of waypoint in real time minutes
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


################## SOUND EFFECTS DEFINITIONS ######################

SFX_INTERVAL = 0.4 # maximum time between sfx (minutes)
# SFX Library
SOUND_CLIPS = {
                'clip00':('silence.wav', 2.0),
                'clip01':('harbor_sounds1.wav', 1.111),
               }

# SFX Groups
A1 = ('clip00') # silence

A3 = ('clip01',
      'clip02',
      'ETC')
