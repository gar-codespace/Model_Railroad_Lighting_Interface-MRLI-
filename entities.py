# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM
from micropython import const as CONST
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as ASYNCIO

# hardware libraries
from hw_ssd1306 import SSD1306_I2C
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button

# local libraries

# splash screen
SPLASH_SCREEN = ['Metropolitan', 'Union', 'Transfer', 'Terminal', 'M.U.T.T.']

# Raspi Pico GP pin assignments
RASPI_PIN = {
        'NA':0,
        'NA':1,
        'NA':2,
        'NA':3,
        'NA':4,
        'BANK0':5,
        'BANK1':6,
        'BANK2':7,
        'BANK3':8,
        'BANK4':9,
        'BANK5':10,
        'RED':11,
        'GREEN':12,
        'BLUE':13,
        'WARM':14,
        'WHITE':15,
        'SDA':16,
        'SCL':17,
        'PSH':18,
        'CONFIRM':19,
        'BACK':20,
        'TRA':21,
        'TRB':22,
        'NA':23,
        'NA':24,
        'NA':25,
        'NA':26,
        'NA':27,
        'NA':28
        }
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
PWM_FREQ = 1000

P_BUTTONS = {'confirm':19, # part of the integrated display
             'back':20 # part of the integrated display
             }

P_OLED0 = {'sda':16, 'scl': 17} # Pins 4 and 5 are the default for the Pico
P_OLED1 = {'sda':0, 'scl': 0}
P_ROTARY = {'psh':18, 'tra':21, 'trb':22} # pin labels for the encoder I'm using
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
CURRENT_ROUTINE = 0 # this gets changed by asyncio

# routine parameters
OFF = {'name':'Off',
        'bank0':(0, 0),
        'bank1':(0, 0),
        'bank2':(0, 0),
        'bank3':(0, 0),
        'bank4':(0, 0),
        'bank5':(0, 0),
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
        'bank5':(0, 0),
        'red':(0, 0, 0),
        'green':(0, 0, 0),
        'blue':(0, 0, 0),
        'warm':(80, 80, 80),
        'white':(20, 20, 20),
        'duration':0,
        'loop':1
           }

TWLIGHT = {'name':'Twlight',
           'bank0':(1, 1),
           'bank1':(1, 1),
           'bank2':(1, 1),
           'bank3':(1, 1),
           'bank4':(1, 1),
           'bank5':(1, 1),
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
           'bank5':(1, 1),
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
           'bank5':(1, 1),
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
           'bank5':(1, 1),
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
           'bank5':(1, 1),
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
           'bank5':(1, 1),
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
           'bank5':(1, 1),
           'red':(0, 0, 0),
           'green':(0, 0, 0),
           'blue':(0, 0, 0),
           'warm':(40, 40, 40),
           'white':(0, 0, 0),
           'duration':0,
           'loop':0
           }