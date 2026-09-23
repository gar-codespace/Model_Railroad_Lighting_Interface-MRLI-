'''
All the settings for the program are here.
All the imports are in one place.
'''

__version__ = '20260901.1.1'
__repo__ = 'https://github.com/gar-codespace/Diorama_Lighting_Automation'

###### PICK A DISPLAY DRIVER ######

# Choose this for the 1.3 inch display
DISPLAY_LIBRARY = 'hw_sh1106'

# Choose this for the 0.9 inch display
# DISPLAY_LIBRARY = 'hw_ssd1306'

SOUND_LIBRARY = 'hw_adafruit_audio_fx'

# packaged libraries
from machine import Pin as PIN, I2C, Timer as TIMER, PWM, UART
from micropython import const as CONST
from random import randint as RANDINT
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as UASYNCIO

# hardware libraries (3rd party)
from hw_rotary_encoder import RotaryEncoder, RotaryEncoderEvent, RotaryEncoderRP2
from hw_button import Button
DISPLAY_DRIVER = __import__(DISPLAY_LIBRARY).Driver_I2C
SOUND_DRIVER = __import__(SOUND_LIBRARY).SoundFX

################## HARDWARE ######################

################## RASPI PICO PARAMETERS ######################

LED = PIN('LED', PIN.OUT)
PWM_FREQ = 480
PWM_STEPS = 65535

################## RASPI PICO PIN ASSIGNMENTS ######################

PICO_PIN = {
        'RED':26, # pwm colors
        'GREEN':27,
        'BLUE':28,
        'WARM':3,
        'COOL':4,

        'SCENIC_R':5, # relays
        'BANK_4_R':6,
        'BANK_3_R':7,
        'BANK_2_R':8,
        'BANK_1_R':9,
        'BANK_0_R':10,

        'SCENIC_B':11, # buttons
        'BANK_4_B':12,
        'BANK_3_B':13,
        'BANK_2_B':14,
        'BANK_1_B':15,
        'BANK_0_B':16,
        'CONFIRM' :22, # encoder
        
        'PSH':17, # encoder
        'TRA':18, # encoder
        'TRB':19, # encoder

        'SDA':20, # I2C
        'SCL':21, # I2C

        'TX'   :0, # UART
        'RESET':1, # SFX board

        'AVAILABLE':2,
        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        }

################## SERIAL COMMUNICATION PROTOCOLS ######################

I2C0 = {
          'ID':0,
          'FREQ':400000
        }

UART0 = {
          'ID':0,
          'BAUD_RATE':9600
        }

################## OLED CONFIGURATIONS ######################

OLED0 = {
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        }

################## MAIN DISPLAY ######################

MAIN_DISPLAY = OLED0
MAIN_DISPLAY_BRIGHT = 70
MAIN_DISPLAY_DIM = 1
MAIN_DISPLAY_BRIGHTNESS = MAIN_DISPLAY_BRIGHT

MAIN_FORMAT =  {
                'LINE_HEIGHT': 10,
                'ROWS': 6,
                'X_OFFSET': 4
                }

################## SOUND HARDWARE ######################

SB0 = { # Adafruit Sound FX Board
        'VOLUME':100,
        'MIN_VOL':0,
        'MAX_VOL':204,
        'MIN_WAIT':30 # milleseconds
        }

MAIN_SOUND_CARD = SB0

################## SOFTWARE ######################

################## TIME BASE ######################

FAST_TIME_CLOCK = 8 # used in model railroading to compress time.
DEFAULT_CYCLE = 20 # milliseconds used for other awaits
START_TIME = 0 # Used for the waypoint duration measurement.
END_TIME = 0 # Used for the waypoint duration measurement.

################## NAVIGATION ######################

MACHINE_STATE = None
STANDBY_TOGGLE = None

WELCOME_SCREEN = ['   M.U.T.T.',
                  ' Metropolitan',
                  '    Union',
                  '   Transfer',
                  '   Terminal'
                  ] # 6 lines maximum, 15 char per line

MAIN_MENU = { # In the order they show on the display
             0: ('| Maintenance',        'STATIC',  1),
             1: ('| Daytime',            'STATIC',  2),
             2: ('| Overcast',           'STATIC',  3),
             3: ('| Twilight',           'STATIC',  5),
             4: ('| Nightime',           'STATIC',  4),
             5: ('> 11PM',            'ALL_DAY',  0),
             6: ('> 3AM',             'ALL_DAY',  2),
             7: ('> 7AM',             'ALL_DAY',  4),
             8: ('> 11AM',            'ALL_DAY',  6),
             9: ('> 3PM',             'ALL_DAY',  8),
            10: ('> 7PM',             'ALL_DAY', 10),
            11: ('> A Cloudy Day',     'CLOUDY',  0),
            12: ('> Stormy Night',     'STORMY',  0)
            }

HIGHLIGHT_ROW = 2 # which row is hilighted when scrolling effects
HILIGHTED_EFFECT = 1 # MAIN_MENU key
CURRENT_EFFECT = MAIN_MENU[HILIGHTED_EFFECT] # Must be a STATIC effect
MENU_FIRST_ITEM: int # calculated on startup by model.get_menu_first_item()
STARTUP_EFFECT_LENGTH = 5000 # Milliseconds

STATIC_SELECT_ROW = 3 # In STATIC state, the encoder moves the rectangle up and down
EDIT_SCREEN_ITEMS = [
                 'WP_NAME',
                 'RED',
                 'GREEN',
                 'BLUE',
                 'WARM',
                 'COOL'
                ]

PWM_TICKS = 100 # How many ticks per indent of the rotary encoder when changing color values.
                # Smaller is finer control.

################## BUFFERS ######################

WORKING_BUFFER = {} # Either the static dictionary or one of the animated dictionaries is copied into this.

################## EFFECT BUFFER ######################
# The running effect writes to and reads from this buffer.
# In STATIC state user inputs are written here.
# The slower the clock cycle, the more accurate the delay.
CLOCK_CYCLE = 500 # Milliseconds per cycle. The delay the lighting effect awaits.
CLOCK_OFFSET = 1 # Adjustment to keep the effect times closer to what they should be.
                 # Adjusts for asyncio overhead slowing down the effects.
RED     = 32500 # PWM value
GREEN   = 32500
BLUE    = 32500
WARM    = 32500
COOL    = 32500
BANK_0  = 1 # 1 is on, 0 is off
BANK_1  = 1
BANK_2  = 1
BANK_3  = 1
BANK_4  = 1
SCENIC  = 1
WP_DUR  = 1 # waypoint_duration is the number of times the effect will await, given a delay of entities.CLOCK_CYCLE
WP_NAME = 'name'
NEXT_WP = 0 # Index of the next waypoint
SFX_GRP = None
STEP_R  = 0 # how much in pwm steps does each color change per CLOCK_CYCLE. pos or neg
STEP_G  = 0
STEP_B  = 0
STEP_W  = 0
STEP_C  = 0
################## EFFECT BUFFER ######################


################## LIGHTING EFFECT DEFINITIONS ######################

'''
In the dictionary for each effect, the duration of the effect is given in real time minutes,
the time the effect actually takes in the real world.
The duration is then adjusted for model railroad 'scale' and converted to milliseconds.

SINGLES effects have one waypoint. The duration is defined as 0, since 'infinately long' seems rediculous.
The random value is a float between 0 and 1. 0 is not random, 1 is maximum randomness.
'''

SINGLES = {
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stby', 'Maint',   'Day',   'Fog', 'Night', 'Twili'), # Waypoint name
'GROUP':  (   'A1',    'A1',    'A3',    'A3',    'A4',    'A5'), # sound effects group
'FRAME':  (      1,       1,       1,       1,       1,       1), # Keyframe marker
'TIME':   (      0,       0,       0,       0,       0,       0), # duration of waypoint
'RANDOM': (     .0,      .0,      .0,      .0,      .0,      .0),

'RED':    [      0,       0,       0,       0,       0,      .1],
'GREEN':  [      0,       0,       0,       0,       0,      .1],
'BLUE':   [      0,       0,       0,       0,    .002,       0],
'WARM':   [      0,     .99,     .22,    .002,       0,     .05],
'COOL':   [      0,     .99,     .02,    .002,    .002,       0],

'BANK_0': [      1,       1,       1,       1,       0,      0,],
'BANK_1': [      0,       1,       0,       0,       0,      0,],
'BANK_2': [      0,       1,       1,       0,       0,      0,],
'BANK_3': [      0,       0,       1,       0,       0,      0,],
'BANK_4': [      0,       1,       1,       1,       1,      1,],
'SCENIC': [      0,       1,       0,       1,       1,      1,],
}

################## ANIMATED LIGHTING EFFECTS ######################

# Each column of an animated effect is being called a waypoint
ALL_DAY = { # simulates an entire day
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : .864,
'NAME':   ( '23:00', '01:00', '03:00', '05:00', '07:00', '09:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00'), # Waypoint name
'GROUP':  (    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3',    'A3'), # sound effects group
'FRAME':  (       1,       0,       1,       0,       1,       0,       1,       0,       1,       0,       1,       0), # Keyframe marker
'TIME':   (     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120), # duration of waypoint in real time minutes
'RANDOM': (      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0), 

'RED':    [    0.00,    0.00,    0.00,    .000,    .004,    0.02,    0.00,    0.00,    0.00,    .003,    .006,    .003],
'GREEN':  [    0.00,    0.00,    0.00,    0.00,    .006,    0.02,    0.00,    0.00,    0.00,    .002,    .004,    0.00],
'BLUE':   [    .001,   .0005,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00],
'WARM':   [    0.00,    0.00,    0.00,    .000,    .005,    0.12,    0.18,    0.18,    0.22,    0.10,    .005,    0.00],
'COOL':   [    .001,    .001,    .001,    0.00,    0.00,    0.01,    0.02,    0.03,    0.02,    .001,    0.00,    .000],

'BANK_0': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_1': [       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0],
'BANK_2': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_3': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_4': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'SCENIC': [       1,       1,       1,       1,       1,       0,       0,       0,       0,       1,       1,       1],
}

STORMY = { # Simulates a stormy night
'CLOCK_CYCLE'  : 8,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stormy','Roll Out',  'Clear', 'Roll In'), # Waypoint name
'GROUP':  (    'D1',       'D1',     'D1',      'D1'), # sound effects group
'FRAME':  (       1,          1,        1,         2), # Keyframe marker
'TIME':   (     1.0,        1.2,      1.0,       1.2), # duration of waypoint in minutes
'RANDOM': (      .8,         .8,       .8,        .8),
'RED':    [    0.00,       0.00,     0.00,      0.00],
'GREEN':  [    0.00,       0.00,     0.00,      0.00],
'BLUE':   [   .0035,      .0035,    .0035,     .0035],
'WARM':   [    0.00,       0.00,     0.00,      0.00],
'COOL':   [    .000,       .000,    .0008,     .0008],
'BANK_0': [       0,          0,        0,         0],
'BANK_1': [       0,          0,        0,         0],
'BANK_2': [       0,          0,        0,         0],
'BANK_3': [       0,          0,        0,         0],
'BANK_4': [       1,          1,        1,         1],
'SCENIC': [       1,          1,        1,         1],
}

CLOUDY = { # Simulates a cloudy day
'CLOCK_CYCLE'  : 25,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Clear','Roll In', 'Cloudy','Roll Out'), # Waypoint name
'GROUP':  (    'A3',     'A3',     'A3',      'A3'), # sound effects group
'FRAME':  (       1,        1,        1,         1), # Keyframe marker
'TIME':   (       4,      3.5,      2.5,       3.5), # duration of waypoint in real time minutes
'RANDOM': (      .7,       .7,       .7,        .7),

'RED':    [    0.00,     0.00,     0.00,      0.00],
'GREEN':  [    0.00,     0.00,     0.00,      0.00],
'BLUE':   [    0.00,     0.00,     0.00,      0.00],
'WARM':   [     .22,      .22,     .045,      .045],
'COOL':   [     .02,      .02,     .026,      .026],

'BANK_0': [       1,        1,        1,         1],
'BANK_1': [       0,        0,        0,         0],
'BANK_2': [       1,        1,        1,         1],
'BANK_3': [       1,        1,        1,         1],
'BANK_4': [       1,        1,        1,         1],
'SCENIC': [       0,        0,        0,         0],
}

################## SOUND EFFECTS DEFINITIONS ######################

PAD_MIN = 2000 # Pad is the time between sound effects in ms
PAD_MAX = 20000 # maximum time between sfx (ms)

SFX_LIBRARY = {  # File    Name,       Duration, Description
                'clip00':('SILENCE0OGG', 10, 'Silence01',   None),
                'clip01':('GULLS001OGG', 16, 'Seagulls 1',  None),
                'clip02':('GULLS002OGG', 9,  'Seagulls 2',  None),
                'clip03':('GULLS003OGG', 8,  'Seagulls 3',  None),
                'clip04':('GULLS004OGG', 13, 'Seagulls 4',  None),
                'clip05':('GULLS005OGG', 20, 'Seagulls 5',  None),
                'clip06':('BELL0001OGG', 6,  'Bells 1',     None),
                'clip07':('BELL0002OGG', 5,  'Bells 2',     None),
                'clip08':('BELL0003OGG', 3,  'Bells 3',     None),
                'clip09':('WHISTLE1OGG', 3,  'Whistle 1',   None),
                'clip10':('WELCOME1OGG', 10, 'Welcome 1',   None),
                'clip11':('BRODY001OGG',  2, 'Brody 1',     None),
                'clip12':('TRAIN001OGG', 12, 'Train 1',     None),
                'clip13':('TRAIN002OGG', 12, 'Train 2',     None),
                'clip14':('TRAIN002OGG',  9, 'Train 3',     None),
                'clip15':('HORN0001OGG',  5, 'Horn 1',      None),
                'clip16':('HORN0002OGG',  5, 'Horn 2',      None),
                'clip17':('HORN0003OGG',  5, 'Horn 3',      None),
                'clip18':('CRICKET1OGG',  8, 'Cricket 1',   None),
                'clip19':('CRICKET2OGG',  7, 'Cricket 2',   None),
                'clip20':('MORNING1OGG', 12, 'Morning 1',   None),
                'clip21':('MORNING2OGG', 19, 'Morning 2',   None),
                'clip22':('NIGHT001OGG', 11, 'Night 1',     None),
                'clip23':('OWL00001OGG',  1, 'Owl 1',       None),
                'clip24':('OWL00002OGG',  3, 'Owl 2',       None),
                'clip25':('THUNDER0OGG',  9, 'Thunder 0',   None),
                'clip26':('THUNDER1OGG', 12, 'Thunder 1',   None),
                'clip27':('THUNDER2OGG', 18, 'Thunder 2', 'bolt'),
                'clip28':('THUNDER3OGG', 11, 'Thunder 3', 'bolt'),
                'clip29':('THUNDER4OGG', 19, 'Thunder 4', 'bolt'),
                'clip30':('WIND0001OGG', 19, 'Wind 1',      None),
                'clip31':('WIND0002OGG', 19, 'Wind 2',      None),
                'clip32':('BELLS004OGG',  7, 'Bells 4',     None),
                'clip33':('BELLS005OGG',  7, 'Bells 5',     None),
                'clip34':('BELLS006OGG',  6, 'Bells 6',     None),
               } # The name is conformed to the soundboard specification

WELCOME_CLIP = SFX_LIBRARY['clip10'][0] # Welcome

# SFX Groups
A1 = [ # silence
      'clip00'
      ]

A3 = [ # Daytime
      'clip01',
      'clip02',
      'clip03',
      'clip04',
      'clip05',
      'clip06',
      'clip07',
      'clip08',
      'clip09',
      'clip11',
      'clip12',
      'clip13',
      'clip14',
      'clip15',
      'clip16',
      'clip17',
      ]

A4 = [ # Twlight, same as day + crickets + morning
      'clip06',
      'clip07',
      'clip08',
      'clip09'
     ]

A5 = [ # Night time, daytime - gulls + crickets + owles
      'clip06',
      'clip07',
      'clip08',
      'clip09'
     ]

B2 = [
      'clip06',
      'clip07',
      'clip08',
      'clip09'
     ]

D1 = [ # Stormy
      'clip25',
      'clip26',
      'clip27',
      'clip28',
      'clip29',
      ]

################## VISUAL EFFECTS ######################

LIGHTNING = [# pwm, MS
             (1400, 40),
             (1000, 40),
             (800, 40),
             (600, 40),
             (400, 40),
             (1400, 80),
             (1000, 80),
             (800, 80),
             (600, 80),
             (400, 80),
             (1000, 80),
             (600, 80),
             (200, 80),
             (0, 40),
             (0, 80),
             (0, 120),
             (0, 160),
             (0, 240),
             (0, 280)
             ]
