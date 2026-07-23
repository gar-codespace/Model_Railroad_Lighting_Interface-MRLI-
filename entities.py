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
PWM_FREQ = 1000
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
        'NA':26,
        'NA':27,
        'NA':28
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

HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling routines

# Effect parameters
SCREEN_MODE = 'WELCOME' # Can be: WELCOME, AUTOMATIC, MONITOR. MANUAL, ADJUST
WELCOME_SCREEN = ['Metropolitan', 'Union', 'Transfer', 'Terminal', 'M.U.T.T.']
STATUS_HILIGHT_INDEX = 0

# Color Control
PWM_TICKS = 100 # how many ticks per indent of the rotary encoder

LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }

PWM_VALUES = {'RED':32500, # these may be changed interactively by the user
              'GREEN':32500,
              'BLUE':32500,
              'WARM':32500,
              'COOL':32500
              }

# Effect type
EFFECT_TYPE = 'static'

# Animated effects countdown
RED_CLOCK = 0
GREEN_CLOCK = 0
BLUE_CLOCK = 0
WARM_CLOCK = 0
COOL_CLOCK = 0

# Time Base
EFFECTS_TICK = 25 # ms. how often the routine is incremented
DEFAULT_TICK = 250 # ms use this if the routine duration is zero
CLOCK_RATIO = 6

# Effects
CURRENT_EFFECTS = 0 # the routine that is running
SELECTED_EFFECTS = 2 # the routine that is selected by the user
SCROLL_EFFECTS = 0 # the top routine listed in the menu
HILIGHTED_EFFECTS = 0 # the routine on the hilighted row

EFFECTS = {
            0:'OFF',
            1:'MAINTENANCE',
            2:'DAY',
            3:'TWLIGHT',
            4:'NIGHT',
            5:'SUNRISE',
            6:'CLOUDY',
            7:'SUNSET',
            8:'STORMY'
            }

# parameters
OFF =  {'name':'Off',
        'type': 'static',
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

MAINTENANCE =  {'name':'Maintenance',
                'type': 'static',
                'bank0':1,
                'bank1':1,
                'bank2':1,
                'bank3':1,
                'bank4':1,
                'scenic':1,
                'red':[.9],
                'green':[.9],
                'blue':[.9],
                'warm':[.9],
                'cool':[.9],
                'duration':0.0,
                'random':0.0,
                'loop':False
                }

DAY =  {'name':'Daytime',
        'type': 'static',
        'bank0':1,
        'bank1':1,
        'bank2':1,
        'bank3':1,
        'bank4':1,
        'scenic':0,
        'red':[.5],
        'green':[.5],
        'blue':[.5],
        'warm':[.5],
        'cool':[.5],
        'duration':0.0,
        'random':0.0,
        'loop':False
        }

TWLIGHT = {'name':'Twlight',
           'type': 'static',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':[.2],
           'green':[.05],
           'blue':[.2],
           'warm':[.2],
           'cool':[.2],
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

NIGHT =   {'name':'Nightime',
           'type': 'static',
           'bank0':1,
           'bank1':1,
           'bank2':1,
           'bank3':1,
           'bank4':1,
           'scenic':1,
           'red':[0],
           'green':[0],
           'blue':[.2],
           'warm':[0],
           'cool':[.2],
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

SUNRISE = {'name':'Sunrise',
           'type': 'animated',
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
           'type': 'animated',
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
           'type': 'animated',
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
           'type': 'animated',
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