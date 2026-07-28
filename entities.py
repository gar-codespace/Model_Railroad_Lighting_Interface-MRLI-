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

# local libraries

# Boilerplate
SCRIPT_REV = CONST('20260704')
TEST_MESSAGE = CONST('abcdefghijklmnopqrstuvwxyz')

###### HARDWARE ######

# Raspi Pico parameters
LED = PIN('LED', PIN.OUT)
PWM_FREQ = 100
PWM_STEPS = 65535

# Raspi Pico GP pin assignments
PICO_PIN = {
        'BANK0_B':0, # buttons
        'BANK1_B':1,
        'BANK2_B':2,
        'BANK3_B':3,
        'BANK4_B':4,
        'SCENIC_B':5,
        'BANK0_S':6, # switches
        'BANK1_S':7,
        'BANK2_S':8,
        'BANK3_S':9,
        'BANK4_S':10,
        'SCENIC_S':11,
        'RED':12, # PWM led
        'GREEN':13,
        'BLUE':14,
        'WARM':15,
        #
        'COOL':16, # 
        'PSH':17, # encoder
        'TRA':18, # encoder
        'TRB':19, # encoder
        'SDA':20, # display
        'SCL':21, # display
        'CONFIRM':22, # encoder
        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        'AVAILABLE':26,
        'AVAILABLE':27,
        'AVAILABLE':28
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

###### SOFTWARE ######

# Time Base
DEFAULT_TICK = 25 # milliseconds
CLOCK_RATIO = 6 # build in some fast time clock compatability

# Navigation
MACHINE = True # True is on False is off
HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling routines
SCREEN_MODE = 'WELCOME' # Can be: WELCOME, AUTOMATIC, MONITOR. MANUAL, ADJUST, OFF
WELCOME_SCREEN = ['Metropolitan', 'Union', 'Transfer', 'Terminal', 'M.U.T.T.']
STATUS_HILIGHT_INDEX = 0
PWM_TICKS = 1000 # how many ticks per indent of the rotary encoder when changing color values
SCROLL_EFFECT = 0 # the top effect listed in the menu

LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }

# Color Control
PWM_STEP = 5 # how much to change pwm value for each color loop cycle

PWM_VALUES = {'RED':32500, # these may be changed interactively by the user
              'GREEN':32500,
              'BLUE':32500,
              'WARM':32500,
              'COOL':32500
              }

###### EFFECTS ######

EFFECT_TYPE = 'STATIC'
SELECTED_EFFECT = 2 # the effect that is selected by the user

# ANIMATED Effects Countdown
RED_CLOCK = 0
GREEN_CLOCK = 0
BLUE_CLOCK = 0
WARM_CLOCK = 0
COOL_CLOCK = 0

EFFECTS = { # the order they appear on the menu
            #0:'OFF',
            0:'MAINTENANCE',
            1:'DAY',
            2:'TWLIGHT',
            3:'NIGHT',
            4:'SUNRISE',
            5:'CLOUDY',
            6:'SUNSET',
            7:'STORMY'
            }

# Machine Control
OFF =  {'name':'Off',
        'type': 'STATIC',
        'bank0':0,
        'bank1':0,
        'bank2':0,
        'bank3':0,
        'bank4':0,
        'scenic':0,
        'red':[0], # the specific color value in decimal percentage
        'green':[0],
        'blue':[0],
        'warm':[0],
        'cool':[0],
        'duration':0.0, # time in minutes
        'random':0.0, # factor to randomize the duration. 0 to 1
        'loop':False
        }

# Effect Parameters
MAINTENANCE =  {'name':'Maintenance',
                'type': 'STATIC',
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
           'bank0':1,
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

CLOUDY =  {'name':'Cloudy Day',
           'type': 'ANIMATED',
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