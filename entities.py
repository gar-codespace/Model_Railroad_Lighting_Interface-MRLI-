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

# constants
SCRIPT_REV = CONST('20260626')
MACHINE_OFF = CONST(0)
MACHINE_ON = CONST(1)
LED = PIN('LED', PIN.OUT)

# OLED
OLED0_ADDRESS = const(0x3C)
OLED1_ADDRESS = const(0x3C)
OLED_WIDTH = CONST(128)
OLED_HEIGHT = CONST(64)
DISPLAY_LINE_HEIGHT = CONST(14)
DISPLAY_ROWS = CONST(5)
DISPLAY_TEST_MESSAGE = CONST('abcdefghijklmnopqrstuvwxyz')

# routines
ROUTINES = {1:'Daytime',
            2:'Twlight',
            3:'Nightime',
            4:'Sunrise',
            5:'Sunset',
            6:'Manual',
            7:'Maintenance',
            8:'Off'}
CURRENT_ROUTINE = 1

# messages
MESSAGES = {1:'Display OK'
            }

# Raspi Pico pin assignments
SWITCHES = (6, 7, 8, 9, 10)
LEDS = (11, 12, 13, 14, 15)
OLED0 = {'sda':16, 'scl': 17} # Pins 4 and 5 are the default for the Pico
OLED1 = {'sda':0, 'scl': 0}
ROTARY = {'push':18, 'dt':19, 'clk':20}

# Configurations
# sda, scl, width, height, addr
DISPLAY0 = (0, OLED0['sda'], OLED0['scl'], OLED_WIDTH, OLED_HEIGHT, OLED0_ADDRESS)
DISPLAY1 = (1, OLED1['sda'], OLED1['scl'], OLED_WIDTH, OLED_HEIGHT, OLED1_ADDRESS)

# local methods
class Initialize:

    def __init__(self):

        self.result = ''

        return
    
    def initializeSwitches(self): # Turn all the switches on
        
        status = ''
        for i in SWITCHES:
            switchX = PIN(i, PIN.OUT)
            switchX.value(MACHINE_ON)
            status += (f"GPIO {switchX} set to {switchX.value()} \n")

        return status
    
    def initializeAll(self):
        
        LED.value(MACHINE_ON)

        self.result += self.initializeSwitches()

        return self.result


def testSwitches() -> None:
    for i in SWITCHES:
        toggleX = PIN(i)
        toggleX.toggle()

def shutDown() -> None:
    for i in SWITCHES:
        switchX = PIN(i)
        switchX.value(MACHINE_OFF)

    for i in LEDS:
        ledX = PIN(i)
        ledX.value(MACHINE_OFF)