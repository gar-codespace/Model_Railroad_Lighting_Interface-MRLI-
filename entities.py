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

# Raspi Pico parameters
LED = PIN('LED', PIN.OUT)
PWM_FREQ = 1000
PWM_STEPS = 65535


# Misc
SCRIPT_REV = CONST('20260704')
MACHINE_OFF = CONST(0)
MACHINE_ON = CONST(1)
TEST_MESSAGE = CONST('abcdefghijklmnopqrstuvwxyz')

# OLED0 specs
OLED0 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
        }
# future capacity
OLED1 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
        }


# OLED Configurations
# bus, width, height, addr, line height, rows, x offset, highlight row
DISPLAY0 = (0, OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])
DISPLAY1 = (1, OLED1['WIDTH'], OLED1['HEIGHT'], OLED1['ADDRESS'])
MAIN_DISPLAY = DISPLAY0
AUX_DISPLAY = DISPLAY1 # Not used, future capacity

# Display formatting
MAIN_FORMAT =  {'LINE_HEIGHT': CONST(13),
                'ROWS': CONST(5),
                'X_OFFSET': 4
                }

# Routine parameters
SCREEN_STATUS = 'WELCOME' # Can be: WELCOME, ROUTINE, STATUS, ADJUST
WELCOME_SCREEN = ['Metropolitan', 'Union', 'Transfer', 'Terminal', 'M.U.T.T.']
STATUS_HILIGHT_INDEX = 0

LED_INDEX_MAP = {0: 'RED',
                 1: 'GREEN',
                 2: 'BLUE',
                 3: 'WARM',
                 4: 'COOL'
                 }

PWM_TICKS = 100
PWM_VALUES = {'RED':10000,
              'GREEN':30000,
              'BLUE':40000,
              'WARM':50000,
              'COOL':60000
              }

ROUTINE_OFFSET = 0.1 # minutes
ROUTINE_TICK = .025 # seconds. How often the routine is updated
DEFAULT_TICK = .25 # use this if the routine duration is zero
CLOCK_RATIO = 6

# Routines
CURRENT_ROUTINE = 2 # this gets changed by the encoder rotation
SELECTED_ROUTINE: int
ROUTINES = {
            0:'OFF',
            1:'MAINTENANCE',
            2:'DAY',
            3:'TWLIGHT',
            4:'NIGHT',
            5:'SUNRISE',
            6:'SUNSET',
            7:'STORMY'
            }

# parameters
OFF =  {'name':'Off',
        'test': 100,
        'bank0':(0, 0), # a specific led strip, begin state, end state
        'bank1':(0, 0),
        'bank2':(0, 0),
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
           'scenic':(1,0),
           'red':(1, 0, 0),
           'green':(1, 0, 0),
           'blue':(.5, 0, 0),
           'warm':(.1, 0, 0),
           'white':(1, 0, 0),
           'duration':0.0,
           'random':0.0,
           'loop':False
           }

MAINTENANCE =  {'name':'Maintenance',
                'test': 300,
                'bank0':(1, 1),
                'bank1':(1, 1),
                'bank2':(1, 1),
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
           'scenic':(1,0),
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
           'scenic':(1,0),
           'red':(0, .1, .4),
           'green':(0, 0, 0),
           'blue':(.4, .1, 0),
           'warm':(0, 0, .7),
           'white':(0, 0, 0),
           'duration':180.0,
           'random':0.0,
           'loop':False
           }

SUNSET =  {'name':'Sunset',
           'test': 800,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'scenic':(1,0),
           'red':(0, 1, 0),
           'green':(0, 1, 0),
           'blue':(0, 1, 0),
           'warm':(1, 0, 1),
           'white':(1, 0, 1),
           'duration':4.0,
           'random':0.0,
           'loop':True
           }

STORMY =  {'name':'Stormy Night',
           'test': 900,
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
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