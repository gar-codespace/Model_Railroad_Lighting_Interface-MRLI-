'''
Entities is the file that has support functions
'''

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
P_SWITCHES = (6, 7, 8, 9, 10)
P_LEDS = (11, 12, 13, 14, 15)
P_OLED0 = {'sda':16, 'scl': 17} # Pins 4 and 5 are the default for the Pico
P_OLED1 = {'sda':0, 'scl': 0}
P_ROTARY = {'push':18, 'dt':19, 'clk':20}

# constants
SCRIPT_REV = CONST('20260626')
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
        }

# Configurations
# sda, scl, width, height, addr
DISPLAY0 = (0, P_OLED0['sda'], P_OLED0['scl'], OLED0['WIDTH'], OLED0['HEIGHT'], OLED0['ADDRESS'])

OLED1_ADDRESS = const(0x3C)

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

def play_routine(routine):

    print(ROUTINES[routine])
