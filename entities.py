'''
Entities is the file that has support functions
'''

# packaged libraries
from machine import Pin as PIN, I2C
from utime import sleep as SLEEP
# from utime import sleep_ms as SLEEP_MS
from micropython import const as CONST
import framebuf as FRAMEBUF

# 3rd party libraries
from ssd1306 import SSD1306_I2C

# local libraries
import interface

# constants
SCRIPT_REV = CONST('20260626')
MACHINE_OFF = CONST(0)
MACHINE_ON = CONST(1)
LED = PIN('LED', PIN.OUT)

# OLED
OLED_ADDRESS1 = const(0x3C)
OLED_ADDRESS0 = const(0x3D)
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
OLED = {'scl': 17, 'sda':16}

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