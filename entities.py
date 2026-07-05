# packaged libraries
from machine import Pin as PIN, I2C
from micropython import const as CONST
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO

# 3rd party libraries
from ssd1306 import SSD1306_I2C
from rotary_encoder import RotaryEncoder, RotaryEncoderEvent
from rotary_encoder_rp2 import RotaryEncoderRP2

# local libraries
import interface

# Raspi Pico pin assignments
P_SWITCHES = {'bank0':5,
              'bank1':6,
              'bank2':7,
              'bank3':8,
              'bank4':9,
              'lights':10
              }

P_LEDS = {'red':11,
          'green':12,
          'blue':13,
          'warm':14,
          'white':15
          }

P_OLED0 = {'sda':16, 'scl': 17} # Pins 4 and 5 are the default for the Pico
P_OLED1 = {'sda':0, 'scl': 0}
P_ROTARY = {'push':18, 'dt':19, 'clk':20}

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
ROUTINES = {0:'Daytime',
            1:'Twlight',
            2:'Nightime',
            3:'Sunrise',
            4:'Sunset',
            5:'Lightning',
            6:'Manual',
            7:'Maintenance',
            8:'Off'}
CURRENT_ROUTINE = 0

# routine parameters
OFF = {'name':'Off',
           'bank0':(False, False),
           'bank1':(False, False),
           'bank2':(False, False),
           'bank3':(False, False),
           'bank4':(False, False),
           'lights':(False, False),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(0, 0, 0),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

DAYTIME = {'name':'Daytime',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(False, False),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(80, 80, 80),
           'white':(20, 20, 20),
           'duration':0,
           'loop': 1
           }

TWLIGHT = {'name':'Twlight',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(100, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

NIGHTIME = {'name':'Nightime',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

SUNRISE = {'name':'Sunrise',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

SUNSET = {'name':'Sunset',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

LIGHTNING = {'name':'Lightning',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':1
           }

MANUAL = {'name':'Manual',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }

MAINTENANCE = {'name':'Maintenance',
           'bank0':(True, True),
           'bank1':(True, True),
           'bank2':(True, True),
           'bank3':(True, True),
           'bank4':(True, True),
           'lights':(True, True),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }