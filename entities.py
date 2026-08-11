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

# Raspi Pico parameters
LED = PIN('LED', PIN.OUT)
PWM_FREQ = 480
PWM_STEPS = 65535
MACHINE = True # True is on False is off

# Raspi Pico GP pin assignments
PICO_PIN = {
        'RED':0, # pwm colors
        'GREEN':1,
        'BLUE':2,
        'WARM':3,
        'COOL':4,

        'SCENIC_S':5, # switches
        'BANK4_S':6,
        'BANK3_S':7,
        'BANK2_S':8,
        'BANK1_S':9,
        'BANK0_S':10,

        'SCENIC_B':11, # buttons
        'BANK4_B':12,
        'BANK3_B':13,
        'BANK2_B':14,
        'BANK1_B':15,
        'BANK0_B':16,
        
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
# future capacity maybe fast time display
OLED1 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
        }

# OLED Configurations (bus, width, height, addr)
DISPLAY0 = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])
DISPLAY1 = (1, OLED1['WIDTH'], OLED1['HEIGHT'], OLED1['ADDRESS'])
MAIN_DISPLAY = DISPLAY0
AUX_DISPLAY = DISPLAY1 # Not used, maybe a fast time clock

# Display formatting
MAIN_FORMAT =  {'LINE_HEIGHT': CONST(13),
                'ROWS': CONST(5),
                'X_OFFSET': 4
                }

# Audio
# Adafruit 9744
SOUND_CARD = {'a':'b', 'c':'d'}

SOUND_CLIPS = {'clip0':'harbor_sounds1.mp3',
               'clip1':'xyzzy.mp3'
               }

###### SOFTWARE ######

# Time Base
DEFAULT_TICK = 20 # milliseconds
CLOCK_RATIO = 6 # build in some fast time clock compatability
CLOCK_CYCLE = 2000 # Milliseconds. The delay the effect awaits.

# Color Control
PWM_STEP = 5 # how much to change pwm value for each color loop cycle

PWM_VALUES = {'RED':32500, # these may be changed interactively by the user
              'GREEN':32500, # or set by the program
              'BLUE':32500,
              'WARM':32500,
              'COOL':32500
              }

# ANIMATED Effects Countdown
RED_CLOCK = 0
GREEN_CLOCK = 0
BLUE_CLOCK = 0
WARM_CLOCK = 0
COOL_CLOCK = 0


####### THE NEW WAY OF SCRIPTING EFFECTS ###########

# Navigation
WELCOME_SCREEN = ['   M.U.T.T.', ' Metropolitan', '    Union', '   Transfer', '   Terminal']
HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling effects
STATIC_SELECT_ROW = 2 # In STATIC mode, the encoder moves the rectangle up and down
DISPLAY_MODE = 'WELCOME' # Can be: welcome, effects, animated, static, edit, standby
DEFAULT_EFFECT = ('Daytime', 'STATIC', 2)
CURRENT_EFFECT = ('Daytime', 'STATIC', 2)
HILIGHTED_EFFECT = 1 # MAIN_MENU key
MENU_FIRST_ITEM = 2 # Index of MAIN_MENU for first item in menu
LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }
PWM_TICKS = 1000 # how many ticks per indent of the rotary encoder when changing color values
STATUS_HILIGHT_INDEX = 0 # What is this?
# Menu
MAIN_MENU = { # In the order they show on the display
             0: ('Maintenance',        'STATIC',  0),
             1: ('Daytime',            'STATIC',  1),
             2: ('Nightime',           'STATIC',  2),
             3: ('Twilight',           'STATIC',  3),
             4: ('* Midnight',       'ANIMATED',  0),
             5: ('* Dawn',           'ANIMATED',  2),
             6: ('* Morning',        'ANIMATED',  4),
             7: ('* Mid Day',        'ANIMATED',  6),
             8: ('* Dusk',           'ANIMATED',  8),
             9: ('* Evening',        'ANIMATED', 10),
            10: ('* A Cloudy Day', 'CLOUDY_DAY',  0)
            }

STATIC = { # 0 duration
'NAME':   ( 'Stby', 'Maint',   'Day', 'Night', 'Twili'),
'INDEX':  (      0,       1,       2,       3,       4),
'TIME':   (      0,       0,       0,       0,       0), # Time of day in minutes
'RANDOM': (     .0,      .0,      .0,      .0,      .0),
'RED':    (      0,     1.0,      .7,      .4,      .2),
'GREEN':  (      0,     1.0,      .7,      .4,      .2),
'BLUE':   (      0,     1.0,      .7,      .4,      .2),
'WARM':   (      0,     1.0,      .7,      .4,      .2),
'COOL':   (      0,     1.0,      .7,      .4,      .2),
'BANK0':  (  False,    True,    True,    True,   True,),
'BANK1':  (  False,    True,    True,    True,   True,),
'BANK2':  (  False,    True,    True,    True,   True,),
'BANK3':  (  False,    True,    True,    True,   True,),
'BANK4':  (  False,    True,    True,    True,   True,),
'SCENIC': (  False,    True,   False,    True,   True,),
}

ANIMATED = { # simulates an entire day
'NAME':   ( '1AM' '3AM', '5AM', '7AM', '9AM','10AM', '1PM', '3PM', '5PM', '7PM', '9PM','11PM'),
'INDEX':  (    0,     1,     2,     3,     4,     5,     6,     7,     8,     9,    10,    11),
'TIME':   (   60,   180,   300,   420,   540,   660,   780,   900,  1020,  1140,  1260,  1380), # Time of day in minutes
'RANDOM': (   .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0,    .0),
'RED':    (  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50),
'GREEN':  (  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50),
'BLUE':   (  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50),
'WARM':   (  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50),
'COOL':   (  .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50,   .50),
'BANK0':  ( True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True),
'BANK1':  ( True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True),
'BANK2':  ( True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True),
'BANK3':  ( True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True),
'BANK4':  ( True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True),
'SCENIC': ( True,  True,  True,  True, False, False, False, False,  True,  True,  True,  True),
}

CLOUDY_DAY = {
'NAME':   ( 'Clear', 'Cloudy',  'Clear'),
'INDEX':  (       0,        1,        2),
'TIME':   (       0,        8,       16), # Time of day in minutes
'RANDOM': (      .5,       .5,       .5),
'RED':    (     .50,       .3,       .5),
'GREEN':  (     .50,       .3,       .5),
'BLUE':   (     .50,       .3,       .5),
'WARM':   (     .50,       .3,       .5),
'COOL':   (     .50,       .3,       .5),
'BANK1':  (    True,     True,     True),
'BANK2':  (    True,     True,     True),
'BANK0':  (    True,     True,     True),
'BANK3':  (    True,     True,     True),
'BANK4':  (    True,     True,     True),
'SCENIC': (   False,    False,    False),
}



##############  THE OLD WAY  ###################

EFFECTS = { # the order they appear on the menu
            0:'MAINTENANCE',
            1:'DAY',
            2:'TWLIGHT',
            3:'NIGHT',
            4:'SUNRISE',
            5:'CLOUDY',
            6:'SUNSET',
            7:'STORMY'
            }

# Effect Parameters
MAINTENANCE =  {'name':'Maintenance',
                'type': 'STATIC',
                'audio': None,
                'bank0':1,
                'bank1':1,
                'bank2':1,
                'bank3':1,
                'bank4':1,
                'scenic':1,
                'red':[1],
                'green':[1],
                'blue':[1],
                'warm':[1],
                'cool':[1],
                'duration':0.0,
                'random':0.0,
                'loop':False
                }

DAY =  {'name':'Daytime',
        'type': 'STATIC',
        'audio': 'clip0',
        'bank0':1,
        'bank1':1,
        'bank2':1,
        'bank3':1,
        'bank4':1,
        'scenic':0,
        'red':[.75],
        'green':[.75],
        'blue':[.75],
        'warm':[.75],
        'cool':[.75],
        'duration':0.0,
        'random':0.0,
        'loop':False
        }

TWLIGHT = {'name':'Twlight',
           'type': 'STATIC',
           'audio': 'clip0',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':[.5],
           'green':[.5],
           'blue':[.5],
           'warm':[.5],
           'cool':[.5],
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

NIGHT =   {'name':'Nightime',
           'type': 'STATIC',
           'audio': 'clip0',
           'bank0':0,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':[.1],
           'green':[.1],
           'blue':[.1],
           'warm':[.1],
           'cool':[.1],
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

SUNRISE = {'name':'Sunrise',
           'type': 'ANIMATED',
           'audio': 'clip0',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':(.8, .5),
           'green':(.8, .5),
           'blue':(.8, .5),
           'warm':(.8, .5),
           'cool':(.8, .5),
           'duration':180.0,
           'random':0.0,
           'loop':False
           }

CLOUDY =  {'name':'* Cloudy Day',
           'type': 'ANIMATED',
           'audio': 'clip0',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':0,
           'red':(.5, 0),
           'green':(.5, 0),
           'blue':(.5, 0),
           'warm':(.5, .8),
           'cool':(.5, .2),
           'duration':5.0,
           'random':0.3,
           'loop':True
           }

SUNSET =  {'name':'Sunset',
           'type': 'ANIMATED',
           'audio': 'clip0',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':(0, 1),
           'green':(0, 1),
           'blue':(0, 1),
           'warm':(1, 0),
           'cool':(1, 0),
           'duration':1.0,
           'random':0.0,
           'loop':False
           }

STORMY =  {'name':'Stormy Night',
           'type': 'ANIMATED',
           'audio': 'clip0',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':(0, 0),
           'green':(0, 0),
           'blue':(0, 0),
           'warm':(.4, .4),
           'cool':(0, 0),
           'duration':5.0,
           'random':0.7,
           'loop':True
           }
