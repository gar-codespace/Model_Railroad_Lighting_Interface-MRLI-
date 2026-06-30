'''
Entities is the file that has support functions
'''

# packaged libraries
from machine import Pin as PIN, I2C
from utime import sleep as SLEEP
from utime import sleep_ms as SLEEP_MS

# 3rd party libraries
from ssd1306 import SSD1306_I2C

# local libraries
import interface

# constants
SCRIPT_REV = '20260626'
MACHINE_OFF = 0
MACHINE_ON = 1
LED = PIN('LED', PIN.OUT)
DISPLAY_LINE_HEIGHT = 14
DISPLAY_ROWS = 5
DISPLAY_TEST_MESSAGE = 'abcdefghijklmnopqrstuvwxyz'
CURRENT_ROUTINE = 1

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

        interface.Display().testDisplay(interface.Display().display())

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