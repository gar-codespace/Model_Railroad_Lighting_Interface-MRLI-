'''
All the settings for the program are here.
Everything is upper case, even though some settings are constants and some are variables.
Oh well. That's what version 2 is for.
Also, I like to keep all the imports in one place.
'''
###### PICK A DISPLAY DRIVER ######

# Choose this for the 1.3 inch display
DISPLAY_DRIVER = 'hw_sh1106'

# Choose this for the 0.9 inch display
# DISPLAY_DRIVER = 'hw_ssd1306'


# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM
from micropython import const as CONST
from time import ticks_ms
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO
import random as RANDOM

# hardware libraries (3rd party)
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button
DISPLAY_LIBRARY = __import__(DISPLAY_DRIVER)

###### HARDWARE ######

########### Raspi Pico parameters

LED = PIN('LED', PIN.OUT)
PWM_FREQ = 480
PWM_STEPS = 65535

########### Raspi Pico GP pin assignments

PICO_PIN = {
        'RED':0, # pwm colors
        'GREEN':1,
        'BLUE':2,
        'WARM':3,
        'COOL':4,

        'SCENIC_S':5, # switches
        'BANK_4_S':6,
        'BANK_3_S':7,
        'BANK_2_S':8,
        'BANK_1_S':9,
        'BANK_0_S':10,

        'SCENIC_B':11, # buttons
        'BANK_4_B':12,
        'BANK_3_B':13,
        'BANK_2_B':14,
        'BANK_1_B':15,
        'BANK_0_B':16,
        
        'PSH':17, # encoder
        'TRA':18, # encoder
        'TRB':19, # encoder
        'SDA':20, # display
        'SCL':21, # display
        'CONFIRM':22, # encoder

        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        'ASDA':26,
        'ASCL':27,
        'BACK':28 # encoder
        }

# OLED0 specs
OLED0 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
        }

# OLED Configurations (bus, width, height, addr)
DISPLAY0 = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])
MAIN_DISPLAY = DISPLAY0
MAIN_DISPLAY_BRIGHTNESS = 70

# Display formatting
MAIN_FORMAT =  {'LINE_HEIGHT': CONST(13),
                'ROWS': CONST(5),
                'X_OFFSET': 4
                }

# Audio

SOUND_CARD = {'a':'b', 'c':'d'}

SOUND_CLIPS = {'clip0':'harbor_sounds1.mp3',
               'clip1':'xyzzy.mp3'
               }

###### SOFTWARE ######

########### Time Base

DEFAULT_TICK = 20 # milliseconds
CLOCK_RATIO = 6 # build in some fast time clock compatability
CLOCK_CYCLE = 2000 # Milliseconds. The delay the effect awaits.

########### Color Control

# Effect Buffer
# The running effect writes to and reads from this buffer
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

# Step Buffer
# how much in pwm steps does each color change per delay cycle. pos or neg
STEP_R = 0
STEP_G = 0
STEP_B = 0
STEP_W = 0
STEP_C = 0

########### Navigation

WELCOME_SCREEN = ['   M.U.T.T.',
                  ' Metropolitan',
                  '    Union',
                  '   Transfer',
                  '   Terminal'
                  ]
HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling effects
STATIC_SELECT_ROW = 2 # In STATIC mode, the encoder moves the rectangle up and down
DISPLAY_MODE = 'WELCOME' # Can be: WELCOME, EFFECTS, ANIMATED, STATIC, EDIT, STANDBY
DEFAULT_EFFECT = ('Daytime', 'STATIC', 2)
CURRENT_EFFECT = ('Daytime', 'STATIC', 2)
HILIGHTED_EFFECT = 1 # MAIN_MENU key
# MENU_FIRST_ITEM is hard coded based on 5 menu lines and the highlite on line 2
# This should be abstracted
MENU_FIRST_ITEM = 10 # Index of MAIN_MENU for first item in menu
LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }
PWM_TICKS = 500 # how many ticks per indent of the rotary encoder when changing color values
STATUS_HILIGHT_INDEX = 0 # What is this?

MAIN_MENU = { # In the order they show on the display
             0: ('Maintenance',        'STATIC',  1),
             1: ('Daytime',            'STATIC',  2),
             2: ('Twilight',           'STATIC',  4),
             3: ('Nightime',           'STATIC',  3),
             4: ('* Midnight',        'ALL_DAY',  0),
             5: ('* Dawn',            'ALL_DAY',  2),
             6: ('* Morning',         'ALL_DAY',  4),
             7: ('* Mid Day',         'ALL_DAY',  6),
             8: ('* Dusk',            'ALL_DAY',  8),
             9: ('* Evening',         'ALL_DAY', 10),
            10: ('* A Cloudy Day',     'CLOUDY',  0)
            }

STATIC_BUFFER = {}

STATIC = {
'NAME':   ( 'Stby', 'Maint',   'Day', 'Night', 'Twili'), # Not used so far
'GROUP':  (   'A1',    'A2',    'A3',    'A4',    'A5'), # Not used so far
'FRAME':  (      0,       1,       2,       3,       4), # Not used so far
'TIME':   (      0,       0,       0,       0,       0), # duration of waypoint
'RANDOM': (     .0,      .0,      .0,      .0,      .0),
'RED':    [      0,       0,       0,       0,      .1],
'GREEN':  [      0,       0,       0,       0,      .1],
'BLUE':   [      0,       0,       0,    .002,       0],
'WARM':   [      0,     1.0,     .20,       0,     .05],
'COOL':   [      0,     1.0,     .05,    .002,       0],
'BANK_0': [      0,       1,       1,       0,      0,],
'BANK_1': [      0,       1,       1,       0,      0,],
'BANK_2': [      0,       1,       1,       0,      0,],
'BANK_3': [      0,       0,       0,       0,      0,],
'BANK_4': [      0,       1,       1,       1,      1,],
'SCENIC': [      0,       0,       0,       0,      0,],
}

ANIMATED_BUFFER = {} # Upon selection, either ALL_DAY or CLOUDY is copied into this

# Each column of an animated effect is being called a waypoint
ALL_DAY = { # simulates an entire day
'NAME':   ('1AM', '3AM', '5AM', '7AM', '9AM','10AM', '1PM', '3PM', '5PM', '7PM', '9PM','11PM'), # Not used so far
'GROUP':  ( 'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1'), # Not used so far
'FRAME':  (    0,     1,     2,     3,     4,     5,     6,     7,     8,     9,    10,    11), # Not used so far
'TIME':   (  120,   120,   120,   120,   120,   120,   120,   120,   120,   120,   120,   120), # duration of waypoint in minutes
'RANDOM': (   .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0), 
'RED':    [  .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15],
'GREEN':  [  .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15],
'BLUE':   [  .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15],
'WARM':   [  .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15],
'COOL':   [  .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15,   .15],
'BANK_0': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
'BANK_1': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
'BANK_2': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
'BANK_3': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
'BANK_4': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1],
'SCENIC': [    1,     1,     1,     1,     0,     0,     0,     0,     1,     1,     1,     1],
}

CLOUDY = { # Simulates a cloudy day
'NAME':   (  'Clear', 'Cloudy'), # Not used so far
'GROUP':  (     'C1',     'C1'), # Not used so far
'FRAME':  (        0,        1), # Not used so far
'TIME':   (        8,        8),
'RANDOM': (       .7,       .7),
'RED':    [        0,        0],
'GREEN':  [        0,        0],
'BLUE':   [        0,        0],
'WARM':   [       .8,     .063],
'COOL':   [      .05,       .2],
'BANK_0': [        1,        1],
'BANK_1': [        1,        1],
'BANK_2': [        1,        1],
'BANK_3': [        0,        0],
'BANK_4': [        1,        1],
'SCENIC': [        0,        0],
}
