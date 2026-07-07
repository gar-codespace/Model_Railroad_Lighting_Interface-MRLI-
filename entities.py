# packaged libraries
from machine import Pin as PIN, I2C
from micropython import const as CONST
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO
import queue as QUEUE

# 3rd party libraries
from ssd1306 import SSD1306_I2C
from rotary_encoder import RotaryEncoder, RotaryEncoderEvent
from rotary_encoder_rp2 import RotaryEncoderRP2

# local libraries
import interface

# Raspi Pico pin assignments
P_SWITCHES = {0:5,
              1:6,
              2:7,
              3:8,
              4:9,
              5:10 # used for model buildings lighting
              }

P_LEDS = {'red':11,
          'green':12,
          'blue':13,
          'warm':14,
          'white':15
          }

P_OLED0 = {'sda':16, 'scl': 17} # Pins 4 and 5 are the default for the Pico
P_OLED1 = {'sda':0, 'scl': 0}
P_ROTARY = {'psh':18, 'tra':19, 'trb':20} # pin labels for the incoder I'm using
# P_ROTARY = {'push':18, 'dt':19, 'clk':20} from the library

# constants
SCRIPT_REV = CONST('20260704')
MACHINE_OFF = CONST(0)
MACHINE_ON = CONST(1)
LED = PIN('LED', PIN.OUT)
TEST_MESSAGE = CONST('abcdefghijklmnopqrstuvwxyz')

# OLED0 specs
OLED0 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
         'ROWS': CONST(5),
         'X_OFFSET': 4
        }

OLED1 = {'ADDRESS': CONST(0x3C),
         'WIDTH': CONST(128),
         'HEIGHT': CONST(64),
         'LINE_HEIGHT': CONST(14),
         'ROWS': CONST(5),
         'X_OFFSET': 4
        }

HIGHLIGHT_RECT = {'LINE2':(0, 24, 128, 15, 1)}
HIGHLIGHT_LINE = {}

# Configurations
# bus, sda, scl, width, height, addr, line height, rows, x offset, highlight row
DISPLAY0 = (0, P_OLED0['sda'], P_OLED0['scl'], OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'], OLED0['LINE_HEIGHT'], OLED0['ROWS'], OLED0['X_OFFSET'], 2)
DISPLAY1 = (1, P_OLED1['sda'], P_OLED1['scl'], OLED1['WIDTH'], OLED1['HEIGHT'], OLED1['ADDRESS'], OLED0['LINE_HEIGHT'], OLED0['ROWS'], OLED0['X_OFFSET'], 2)

MENU_DISPLAY = DISPLAY0
MENU_HIGHLIGHT = HIGHLIGHT_RECT['LINE2']
AUX_DISPLAY = DISPLAY1 # Not used, future capacity

# routines
ROUTINES = {0:'DAY',
            1:'TWLIGHT',
            2:'NIGHT',
            3:'SUNRISE',
            4:'SUNSET',
            5:'STORMY',
            6:'MANUAL',
            7:'MAINTENANCE',
            8:'OFF'}
CURRENT_ROUTINE = 0

# routine parameters
OFF = {'name':'Off',
        'bank0':(0, 0),
        'bank1':(0, 0),
        'bank2':(0, 0),
        'bank3':(0, 0),
        'bank4':(0, 0),
        'lights':(0, 0),
        'red':(0, 0, 0),
        'green':(0, 0, 0),
        'blue':(0, 0, 0),
        'warm':(0, 0, 0),
        'white':(0, 0, 0),
        'duration':0,
        'loop':0
        }

DAY = {'name':'Cloudy Day',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(0, 0),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(80, 80, 80),
           'white':(20, 20, 20),
           'duration':0,
           'loop': 1
           }

TWLIGHT = {'name':'Twlight',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(100, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

NIGHT = {'name':'Nightime',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

SUNRISE = {'name':'Sunrise',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

SUNSET = {'name':'Sunset',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

STORMY = {'name':'Stormy Night',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':1
           }

MANUAL = {'name':'Manual',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

MAINTENANCE = {'name':'Maintenance',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'lights':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }