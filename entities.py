'''
I like to keep all the imports in one place
'''

# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM
from micropython import const as CONST
from time import ticks_ms
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO
import random as RANDOM

# hardware libraries (3rd party)
from hw_ssd1306 import SSD1306_I2C
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button
from hw_MAX9744 import MAX9744

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
# specs for a larger oled display
OLED1 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
        }

# OLED Configurations (bus, width, height, addr)
SMALL_DISPLAY = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])
LARGE_DISPLAY = (0, OLED1['WIDTH'], OLED1['HEIGHT'], OLED1['ADDRESS'])
MAIN_DISPLAY = SMALL_DISPLAY

# Display formatting
MAIN_FORMAT =  {'LINE_HEIGHT': CONST(13),
                'ROWS': CONST(5),
                'X_OFFSET': 4
                }

# Audio
# Adafruit MAX9744
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
RED    = 32500
BLUE   = 32500
WARM   = 32500
COOL   = 32500
BANK_0  = 1 # 1 is on, 0 is off
BANK_1  = 1
BANK_2  = 1
BANK_3  = 1
BANK_4  = 1
SCENIC = 1

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
MENU_FIRST_ITEM = 10 # Index of MAIN_MENU for first item in menu
LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }
PWM_TICKS = 1000 # how many ticks per indent of the rotary encoder when changing color values
STATUS_HILIGHT_INDEX = 0 # What is this?

MAIN_MENU = { # In the order they show on the display
             0: ('Maintenance',        'STATIC',  1),
             1: ('Daytime',            'STATIC',  2),
             2: ('Nightime',           'STATIC',  3),
             3: ('Twilight',           'STATIC',  4),
             4: ('* Midnight',       'ANIMATED',  0),
             5: ('* Dawn',           'ANIMATED',  2),
             6: ('* Morning',        'ANIMATED',  4),
             7: ('* Mid Day',        'ANIMATED',  6),
             8: ('* Dusk',           'ANIMATED',  8),
             9: ('* Evening',        'ANIMATED', 10),
            10: ('* A Cloudy Day',   'ANIMATED', 12)
            }

STATIC_BUFFER = {}

STATIC = {
'NAME':   ( 'Stby', 'Maint',   'Day', 'Night', 'Twili'),
'GROUP':  (   'A1',    'A2',    'A3',    'A4',    'A5'),
'INDEX':  (      0,       1,       2,       3,       4),
'TIME':   (      0,       0,       0,       0,       0), # Time of day in minutes
'RANDOM': (     .0,      .0,      .0,      .0,      .0),
'RED':    [      0,     1.0,      .6,      .4,      .2],
'GREEN':  [      0,     1.0,      .7,      .4,      .2],
'BLUE':   [      0,     1.0,      .7,      .4,      .2],
'WARM':   [      0,     1.0,      .7,      .4,      .2],
'COOL':   [      0,     1.0,      .7,      .4,      .2],
'BANK_0': [      0,       1,       1,       0,      1,],
'BANK_1': [      0,       1,       0,       1,      0,],
'BANK_2': [      0,       1,       1,       0,      0,],
'BANK_3': [      0,       1,       0,       1,      0,],
'BANK_4': [      0,       1,       1,       0,      0,],
'SCENIC': [      0,       1,       0,       1,      1,],
}

ANIMATED = { # simulates an entire day
'NAME':   ( '1AM' '3AM', '5AM', '7AM', '9AM','10AM', '1PM', '3PM', '5PM', '7PM', '9PM','11PM',   'Clear', 'Cloudy',  'Clear'),
'GROUP':  ( 'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',  'B1',      'C1',     'C1',     'C1'),
'INDEX':  (    0,     1,     2,     3,     4,     5,     6,     7,     8,     9,    10,    11,         0,        1,        2),
'TIME':   (   60,   180,   300,   420,   540,   660,   780,   900,  1020,  1140,  1260,  1380,         0,        8,       16), # Time of day in minutes
'RANDOM': (   .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,        .5,       .5,       .5),
'RED':    [  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,       .50,       .3,       .5],
'GREEN':  [  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,       .50,       .3,       .5],
'BLUE':   [  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,       .50,       .3,       .5],
'WARM':   [  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,       .50,       .3,       .5],
'COOL':   [  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,       .50,       .3,       .5],
'BANK_0': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,         1,        1,        1],
'BANK_1': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,         1,        1,        1],
'BANK_2': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,         1,        1,        1],
'BANK_3': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,         1,        1,        1],
'BANK_4': [    1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,     1,         1,        1,        1],
'SCENIC': [    1,     1,     1,     1,     0,     0,     0,     0,     1,     1,     1,     1,         0,        0,        0],
}
