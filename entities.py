'''
I like to keep all the imports in one place
'''

# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM
from micropython import const as CONST
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO
import random as RANDOM

# hardware libraries (3rd party)
from hw_ssd1306 import SSD1306_I2C
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button

# local libraries

# Raspi Pico GP pin assignments
PICO_PIN = {
        'RED_V':0, # pot to manually control red brightness
        'GREEN_V':1,
        'BLUE_V':2,
        'WARM_V':3,
        'WHITE_V':4,
        'BANK0':5, # led bank0 on or off
        'BANK1':6,
        'BANK2':7,
        'BANK3':8,
        'BANK4':9,
        'SCENIC':10,
        'RED':11, # red brightness for all banks
        'GREEN':12,
        'BLUE':13,
        'WARM':14,
        'WHITE':15,
        'SDA':16, # display
        'SCL':17, # display
        'PSH':18, # encoder
        'CONFIRM':19, # part of the integrated display
        'BACK':20, # part of the integrated display
        'TRA':21, # encoder
        'TRB':22, # encoder
        'RESERVED':23,
        'RESERVED':24,
        'LED':'LED',
        'BANK2_B':26, # button to manuallu turn bank2 on or off
        'BANK3_B':27,
        'BANK4_B':28
        }

# Raspi Pico parameters
LED = PIN('LED', PIN.OUT)
PWM_FREQ = 1000
PWM_STEPS = 65535


# Misc
SCRIPT_REV = CONST('20260704')
MACHINE_OFF = CONST(0)
MACHINE_ON = CONST(1)
TEST_MESSAGE = CONST('abcdefghijklmnopqrstuvwxyz')
SPLASH_SCREEN = ['Metropolitan', 'Union', 'Transfer', 'Terminal', 'M.U.T.T.']

# OLED0 specs
OLED0 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
         'ROWS': CONST(5),
         'X_OFFSET': 4
        }
# future capacity
OLED1 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
         'ROWS': CONST(5),
         'X_OFFSET': 4
        }

HIGHLIGHT_RECT = {'LINE0':(0, 0, 128, 15, 1), 'LINE1':(0, 12, 128, 15, 1), 'LINE2':(0, 24, 128, 15, 1)}
HIGHLIGHT_LINE = {} # not used at this time

# OLED Configurations
# bus, width, height, addr, line height, rows, x offset, highlight row
DISPLAY0 = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'], OLED0['LINE_HEIGHT'], OLED0['ROWS'], OLED0['X_OFFSET'], 2)
DISPLAY1 = (1, OLED1['WIDTH'], OLED1['HEIGHT'], OLED1['ADDRESS'], OLED0['LINE_HEIGHT'], OLED0['ROWS'], OLED0['X_OFFSET'], 2)

MENU_DISPLAY = DISPLAY0
MENU_HIGHLIGHT = HIGHLIGHT_RECT['LINE2'] # This doesn't quite work but it's close
AUX_DISPLAY = DISPLAY1 # Not used, future capacity

# Lighting Routines
ROUTINES = {
            0:'OFF',
            1:'MANUAL',
            2:'MAINTENANCE',
            3:'DAY',
            4:'TWLIGHT',
            5:'NIGHT',
            6:'SUNRISE',
            7:'SUNSET',
            8:'STORMY'
            }

CURRENT_ROUTINE = 1 # this gets changed by what exactly?
ROUTINE_OFFSET = 0.1 # minutes
ROUTINE_TICK = 0.025 # seconds. How often the routine is updated
DEFAULT_TICK = 0.25 # use this if the routine duration is zero

# routine parameters
OFF =  {'name':'Off',
        'test': 100,
        'bank0':(0, 0), # a specific led strip, begin state, end state
        'bank1':(0, 0),
        'bank2':(0, 0),
        'bank3':(0, 0),
        'bank4':(0, 0),
        'scenic':(0,0),
        'red':(0, 0, 0), # the specific color, begin value, midpoint value, end value in percentage
        'green':(0, 0, 0),
        'blue':(0, 0, 0),
        'warm':(0, 0, 0),
        'white':(0, 0, 0),
        'duration':0.0, # time in minutes
        'random':0.0, # factor to randomize the duration. 0 to 1
        'loop':False
        }

MANUAL =  {'name':'Manual',
           'test': 200,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(1,0),
           'red':(1, 0, 0),
           'green':(.5, 0, 0),
           'blue':(.5, 0, 0),
           'warm':(5, 0, 0),
           'white':(.5, 0, 0),
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

MAINTENANCE =  {'name':'Maintenance',
                'test': 300,
                'bank0':(1, 1),
                'bank1':(1, 1),
                'bank2':(1, 1),
                'bank3':(1, 1),
                'bank4':(1, 1),
                'scenic':(0,0),
                'red':(1, 0, 0),
                'green':(1, 0, 0),
                'blue':(1, 0, 0),
                'warm':(1, 0, 0),
                'white':(1, 0, 0),
                'duration':0.0,
                'random':0.0,
                'loop':False
                }

DAY =  {'name':'Cloudy Day',
        'test': 400,
        'bank0':(1, 1),
        'bank1':(1, 1),
        'bank2':(1, 1),
        'bank3':(1, 1),
        'bank4':(1, 1),
        'scenic':(0,0),
        'red':(.5, 0, 0),
        'green':(.5, 0, 0),
        'blue':(.5, 0, 0),
        'warm':(.5, .8, .8),
        'white':(.5, .2, .2),
        'duration':5.0,
        'random':0.3,
        'loop':True
        }

TWLIGHT = {'name':'Twlight',
           'test': 500,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(1,0),
           'red':(.2, 0, 0),
           'green':(.05, 0, 0),
           'blue':(.2, 0, 0),
           'warm':(.2, .4, .4),
           'white':(.2, 0, 0),
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

NIGHT =   {'name':'Nightime',
           'test': 600,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(0,0),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(.4, .4, .4),
           'white':(0, 0, 0),
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

SUNRISE = {'name':'Sunrise',
           'test': 700,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(0,0),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(.4, .4, .4),
           'white':(0, 0, 0),
           'duration':30.0,
           'random':0.0,
           'loop':False
           }

SUNSET =  {'name':'Sunset',
           'test': 800,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(0,0),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(.4, .4, .4),
           'white':(0, 0, 0),
           'duration':30.0,
           'random':0.0,
           'loop':False
           }

STORMY =  {'name':'Stormy Night',
           'test': 900,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'scenic':(0,0),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(.4, .4, .4),
           'white':(0, 0, 0),
           'duration':0.0,
           'random':0.0,
           'loop':True
           }