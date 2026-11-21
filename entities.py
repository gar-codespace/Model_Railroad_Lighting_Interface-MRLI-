'''
Model Railroad Lighting Interface (MRLI)

All the settings for the program are here.
All the packaged imports are in one place.
'''

__version__ = '20261001.1.5'

# packaged libraries are kept to a minimum
from machine import Pin as PIN, I2C, PWM, UART
# from machine import Timer as TIMER # Used with hw_rotary_encoder
from micropython import const as CONST
from random import randint as RANDINT
import utime as UTIME
import framebuf as FRAMEBUF
import uasyncio as UASYNCIO


################## LOGGING ######################

LOGGING_MESSAGE:list = [f'Model Railroad Lighting Automation', f'Version: {__version__}']

def log():
      '''Write machine progress somewhere, screen, log, Etc.'''

      global LOGGING_MESSAGE

      if not LOGGING_MESSAGE:
            return

      for message in LOGGING_MESSAGE:
            print(message)

      LOGGING_MESSAGE = []

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
        'CONF_0_B':22, # encoder button
        
        'PSH':17, # encoder
        'TRA':18, # encoder
        'TRB':19, # encoder

        'COM0':20, # I2C SDA
        'COM1':21, # I2C SCL
        'COM2':0, # UART TX
      #   'COM3':1,
      #   'RESET':2,

        'AVAILABLE':1,
        'AVAILABLE':2,
        'RESERVED':23, # WiFi
        'RESERVED':24, # WiFi
        'LED':'LED',
        }

################## SERIAL COMMUNICATION PROTOCOLS ######################

I2C_0 = {
          'TYPE':'i2c',
          'ID':0,
          'SDA':'COM0',
          'SCL':'COM1',
          'FREQ':400000
        }

UART_0 = {
          'TYPE':'uart',
          'ID':0,
          'TX':'COM2',
          'RX':None,
          'FREQ':9600
        }

################## DISPLAY PARAMETERS ######################

OLED_0 = {
        'NAME':'Main Display',
        'MAKE':'Godiymodules',
        'MODEL':'White OLED Display Screen',
        'DRIVER': 'hw_sh1106',
        'SIZE':'1.3 inch',
        'BUS':'i2c',
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        'ROTATE': False,
        'EXTERNAL_VCC':False,
        }

OLED_1 = { 
        'NAME':'Main Display',
        'MAKE':'Godiymodules',
        'MODEL':'White OLED Display Screen',
        'DRIVER': 'hw_ssd1306',
        'SIZE':'0.9',
        'BUS':'i2c',
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        'ROTATE': False,
        'EXTERNAL_VCC':False,
        }

################## DISPLAY DEFINITIONS ######################

DISPLAY_0 = {
            'NAME':'1.3" OLED Display',
            'COM':'I2C_0',
            'PARAMS':'OLED_0',
            }

DISPLAY_1 = {
            'NAME':'0.9" OLED Display',
            'COM':'I2C_0',
            'PARAMS':'OLED_1',
            }

################## SOUND PARAMETERS ######################

SB_0 = {
       'NAME':'Sound Card',
       'MAKE': 'Adafruit',
       'MODEL': 'Sound FX Board',
       'DRIVER': 'hw_adafruit_audio_fx',
       'SIZE':'16mB',
       'BUS':'UART',
       'WAIT':50,
       'DUPLEX':False,
       'RESET':False,
       }

################## SOUND DEFINITIONS ######################

SOUND_CARD_0 = {
            'NAME': 'Adafruit Sound Effects Card',
            'COM':'UART_0',
            'PARAMS':'SB_0',
            }

################## ENCODER PARAMETERS ######################

ENCODER_0 = {
            'DRIVER': 'hw_rotary_encoder',
            'MODE': 'IN',
            'PULL': 'PULL_UP',
            'TRA': 'TRA',
            'TRB': 'TRB',
            'PSH': 'PSH',
            'DEBOUNCE_MS':50, # filter out pin jitter
            'ENCODER_STEP':1, # filter out pin jitter
            'HALF_STEP':False,# support increment every click for KY040 encoder
            'ONE_STEP_MS':15, # It is a crunch, but it works for now
            'CLICK_MS':400, # detect a single click
            'STEP_MS':200, # detect a multiple press
            'LONG_MS':1000, # detect a long press
            'FAST_MS':50, # detect a fast encoder turn
            }

################## PUSH BUTTON PARAMETERS ######################

BUTTON_0 = {
            'DRIVER': 'hw_push_button',
            'MODE': 'IN',
            'PULL': 'PULL_UP',
            'IRQ_TRIGGER':True, # False for asyncio trigger
            'DEBOUNCE_TIME':40,
            'MULTI_TIME':350,
            'LONG_TIME':800,
            'RELEASED_MSG':'button released',
            'MULTI_MSG':'multiple presses',
            'LONG_MSG':'long press'
            }

################## SOFTWARE ######################

################## DISPLAY SETTINGS ######################

DISPLAY_BRIGHT = 70
DISPLAY_DIM = 1
MAIN_DISPLAY_BRIGHT = DISPLAY_BRIGHT

MAIN_FORMAT =  {
                'LINE_HEIGHT': 10, # Pixels
                'ROWS': 6,
                'CHAR_PER_ROW':15,
                'X_OFFSET': 2, # Pixels
                'Y_OFFSET': 2, # Pixels
                }

################## TIME BASE ######################

FAST_TIME_CLOCK = 8 # used in model railroading to compress time.
DEFAULT_CYCLE = 20 # milliseconds used for other awaits
WAYPOINT_START = 0 # Used for the waypoint duration measurement.
WAYPOINT_END = 0 # Used for the waypoint duration measurement.
WAYPOINT_RUN_TIME = 0 # Time the waypoint actually ran (seconds)

################## NAVIGATION ######################

MACHINE_STATE:str  = None
STANDBY_TOGGLE:str = None

STARTUP_EFFECT_DURATION = 5000 # Milliseconds
WELCOME_SCREEN = ['M.U.T.T.', 'Metropolitan', 'Union ', 'Transfer', 'Terminal'] # 6 lines maximum, 15 char per line

EFFECTS_MENU = { #     Name             Type    Index
             0: ('Maintenance',  'SINGLES',  1),
             1: ('Daytime',      'SINGLES',  2),
             2: ('Overcast',     'SINGLES',  3),
             3: ('Twilight',     'SINGLES',  5),
             4: ('Nightime',     'SINGLES',  4),
             5: ('11PM',         'ALL_DAY',  0),
             6: ('3AM',          'ALL_DAY',  2),
             7: ('7AM',          'ALL_DAY',  4),
             8: ('11AM',         'ALL_DAY',  6),
             9: ('3PM',          'ALL_DAY',  8),
            10: ('7PM',          'ALL_DAY', 10),
            11: ('A Cloudy Day',  'CLOUDY',  0),
            12: ('Stormy Night',  'STORMY',  0)
            } # In the order they show on the display
EFFECTS_HIGHLIGHT_ROW = 2 # which row is hilighted
EFFECTS_HILIGHTED_EFFECT = 1 # EFFECTS_MENU key and default effect
EFFECTS_MENU_FIRST_ITEM:int # calculated on startup by model.get_menu_first_item()
EFFECTS_MENU_STATIC_SYMBOL = '|'
EFFECTS_MENU_ANIMATED_SYMBOL = '>'
CURRENT_EFFECT = EFFECTS_MENU[EFFECTS_HILIGHTED_EFFECT] # Must be a STATIC effect. Also used as the default effect.
EFFECTS_RECT = [0, 'y', 128, 12, 1]

STATIC_SELECT_ROW = 3 # In STATIC state, the encoder moves the rectangle up and down
STATIC_RECT = [0, 'y', 128, 12, 1]

EDIT_ROUNDING_VALUE = 4
EDIT_SCREEN_ITEMS = [
                 'WP_NAME',
                 'RED',
                 'GREEN',
                 'BLUE',
                 'WARM',
                 'COOL'
                ]
EDIT_RECT = [54, 'y', 74, 12, 1]
EDIT_PWM_TICKS = 10 # How many ticks per indent of the rotary encoder when changing color values.
                    # Smaller is finer control.

################## BUFFERS ######################

WORKING_BUFFER = {} # Either the static dictionary or one of the animated dictionaries is copied into this.

################## EFFECT BUFFER ######################

CLOCK_CYCLE = 500 # Milliseconds. WP_DUR * CLOCK_CYCLE = waypoint time
CLOCK_OFFSET = 1 # Adjusts for asyncio overhead. Smaller = faster.
                 
RED     :int = 32500 # PWM value
GREEN   :int = 32500
BLUE    :int = 32500
WARM    :int = 32500
COOL    :int = 32500
BANK_0  :int = 1 # 1 is on, 0 is off
BANK_1  :int = 1
BANK_2  :int = 1
BANK_3  :int = 1
BANK_4  :int = 1
SCENIC  :int = 1
CUR_WP  :int = None
WP_DUR  :int = 1
NEXT_WP :int = 0 # Index of the next waypoint
WP_NAME :str = 'name'
HOUR  :float = 0.0 # Fast time clock display
TIME    :int = 0
CLIP  :tuple = None # sound clip
CLIP_G  :str = None # the name of the group, not the members
STEP_R  :int = 0 # how much in pwm steps does each color change per CLOCK_CYCLE. pos or neg
STEP_G  :int = 0
STEP_B  :int = 0
STEP_W  :int = 0
STEP_C  :int = 0
STEP_H:float = 0.0 # Increment the hour
################## EFFECT BUFFER ######################


################## LIGHTING EFFECT DEFINITIONS ######################

SINGLES = {
'E_NAME': 'Static Effect Collection',
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Dark', 'Maint',   'Day',   'Ovcst', 'Night', 'Twili'), # Waypoint name
'GROUP':  (   'A1',    'A1',    'A3',      'A3',    'A5',    'A4'), # sound effects group
'HOUR':   (      0,       0,       0,         0,       0,       0),
'TIME':   (      0,       0,       0,         0,       0,       0), # duration of waypoint
'RANDOM': (     .0,      .0,      .0,        .0,      .0,      .0),
'RED':    [      0,       0,       0,         0,       0,    .004],
'GREEN':  [      0,       0,       0,         0,       0,    .006],
'BLUE':   [      0,       0,       0,         0,   .0035,       0],
'WARM':   [      0,     .99,     .22,      .002,       0,    .005],
'COOL':   [      0,     .99,     .02,      .002,   .0008,       0],
'BANK_0': [      0,       1,       1,         1,       0,      0,],
'BANK_1': [      0,       1,       0,         0,       0,      0,],
'BANK_2': [      0,       1,       1,         0,       0,      0,],
'BANK_3': [      0,       0,       1,         0,       0,      0,],
'BANK_4': [      0,       1,       1,         1,       1,      1,],
'SCENIC': [      0,       1,       0,         1,       1,      1,],
}

################## ANIMATED LIGHTING EFFECTS ######################

# Each column of an animated effect is being called a waypoint
ALL_DAY = {
'E_NAME': 'A Complete Day',
'CLOCK_CYCLE'  : 250,
'CLOCK_OFFSET' : .859, # Smaller is faster
'NAME':   ( '23:00', '01:00', '03:00', '05:00', '07:00', '09:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00'), # Waypoint name
'GROUP':  (    'A5',    'A5',    'A5',    'A4',    'A3',    'A3',    'A3',    'A3',    'A3',    'A4',    'A4',    'A5'), # sound effects group
'HOUR':   (      23,       1,       3,       5,       7,       9,      11,      13,      15,      17,      19,      21), # the time of day
'TIME':   (     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120,     120), # duration of waypoint in real time minutes
'RANDOM': (      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0,      .0), 
'RED':    [    0.00,    0.00,    0.00,    .000,    .004,    0.02,    0.00,    0.00,    0.00,    .003,    .006,    .003],
'GREEN':  [    0.00,    0.00,    0.00,    0.00,    .006,    0.02,    0.00,    0.00,    0.00,    .002,    .004,    .002],
'BLUE':   [    .001,   .0005,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00,    0.00],
'WARM':   [    0.00,    0.00,    0.00,    .000,    .005,    0.12,    0.18,    0.18,    0.22,    0.10,    .005,    .003],
'COOL':   [    .001,    .001,    .001,    0.00,    0.00,    0.01,    0.02,    0.03,    0.02,    .001,    0.00,    .000],
'BANK_0': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_1': [       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0],
'BANK_2': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_3': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'BANK_4': [       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1,       1],
'SCENIC': [       1,       1,       1,       1,       1,       0,       0,       0,       0,       1,       1,       1],
}

STORMY = {
'E_NAME': 'A Stormy Night',
'CLOCK_CYCLE'  : 8,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Stormy','Roll Out',  'Clear', 'Roll In'), # Waypoint name
'GROUP':  (    'D1',       'D1',     'D1',      'D1'), # sound effects group
'HOUR':   (       0,          0,        0,         0),
'TIME':   (     1.0,        1.2,      1.0,       1.2), # duration of waypoint in minutes
'RANDOM': (      .8,         .8,       .8,        .8),
'RED':    [    0.00,       0.00,     0.00,      0.00],
'GREEN':  [    0.00,       0.00,     0.00,      0.00],
'BLUE':   [   .0035,      .0035,    .0035,     .0035],
'WARM':   [    0.00,       0.00,     0.00,      0.00],
'COOL':   [    .000,       .000,    .0009,     .0009],
'BANK_0': [       0,          0,        0,         0],
'BANK_1': [       0,          0,        0,         0],
'BANK_2': [       0,          0,        0,         0],
'BANK_3': [       0,          0,        0,         0],
'BANK_4': [       1,          1,        1,         1],
'SCENIC': [       1,          1,        1,         1],
}

CLOUDY = {
'E_NAME': 'A Cloudy Day',
'CLOCK_CYCLE'  : 25,
'CLOCK_OFFSET' : 1,
'NAME':   ( 'Clear','Roll In', 'Cloudy','Roll Out'), # Waypoint name
'GROUP':  (    'A3',     'A3',     'A3',      'A3'), # sound effects group
'HOUR':   (       0,        0,        0,         0),
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

################## AMBIENT SOUND DEFINITIONS ######################

PAD_MIN = 2000 # Pad is the time between ambient sound (ms)
PAD_MAX = 20000 # maximum time between ambient sounds (ms)
WELCOME_CLIP = 'clip10'
STANDBY_IN_CLIP = 'clip23'
STANDBY_OUT_CLIP = 'clip09'
PAUSE_CLIP = None
UNPAUSE_CLIP = None
CLIP = WELCOME_CLIP

AMBIENCE = { 
            'NAME': 'The library of sound effects',
              #  File      Name,    Duration, Description   VFX   Vol flag
                'clip00':('SILENCE0OGG', 10, 'Silence',     None),
                'clip01':('GULLS001OGG', 16, 'Seagulls 1',  None),
                'clip02':('GULLS002OGG',  9, 'Seagulls 2',  None),
                'clip03':('GULLS003OGG',  8, 'Seagulls 3',  None),
                'clip04':('GULLS004OGG', 13, 'Seagulls 4',  None),
                'clip05':('GULLS005OGG', 20, 'Seagulls 5',  None),
                'clip06':('BELL0001OGG',  6, 'Bells 1',     None, 1),
                'clip07':('BELL0002OGG',  5, 'Bells 2',     None, 1),
                'clip08':('BELL0003OGG',  3, 'Bells 3',     None, 1),
                'clip09':('WHISTLE1OGG',  3, 'Whistle 1',   None, 1),
                'clip10':('WELCOME1OGG',  6, 'Welcome',     None),
                'clip11':('BRODY001OGG',  2, 'Brody 1',     None, 1),
                'clip12':('TRAIN001OGG', 12, 'Train 1',     None),
                'clip13':('TRAIN002OGG', 12, 'Train 2',     None),
                'clip14':('TRAIN002OGG',  9, 'Train 3',     None),
                'clip15':('HORN0001OGG',  5, 'Horn 1',      None), # Not used
                'clip16':('HORN0002OGG',  5, 'Horn 2',      None),
                'clip17':('HORN0003OGG',  5, 'Horn 3',      None),
                'clip18':('CRICKET1OGG',  8, 'Cricket 1',   None),
                'clip19':('CRICKET2OGG',  7, 'Cricket 2',   None),
                'clip20':('MORNING1OGG', 12, 'Morning 1',   None),
                'clip21':('MORNING2OGG', 19, 'Morning 2',   None),
                'clip22':('NIGHT001OGG', 11, 'Night 1',     None),
                'clip23':('OWL00001OGG',  1, 'Owl 1',       None, 1),
                'clip24':('OWL00002OGG',  3, 'Owl 2',       None, 1),
                'clip25':('THUNDER0OGG',  9, 'Thunder 0',   None),
                'clip26':('THUNDER1OGG', 12, 'Thunder 1',   None),
                'clip27':('THUNDER2OGG', 18, 'Thunder 2', 'bolt'),
                'clip28':('THUNDER3OGG', 11, 'Thunder 3', 'bolt'),
                'clip29':('THUNDER4OGG', 19, 'Thunder 4', 'bolt'),
                'clip30':('WIND0001OGG', 19, 'Wind 1',      None),
                'clip31':('WIND0002OGG', 19, 'Wind 2',      None),
                'clip32':('BELLS004OGG',  7, 'Bells 4',     None, 1),
                'clip33':('BELLS005OGG',  7, 'Bells 5',     None, 1),
                'clip34':('BELLS006OGG',  6, 'Bells 6',     None, 1),
                'clip35':('HORN0004OGG',  5, 'Horn 4',      None, 1),
                'clip36':('HORN0005OGG',  5, 'Horn 5',      None, 1),
                'clip37':('GEESE001OGG',  7, 'Geese 1',     None),
                'clip38':('GEESE002OGG',  7, 'Geese 2',     None),
                'clip39':('GULLS006OGG',  8, 'Seagulls 6',  None), # Same as Seagulls 1
               } # The name is conformed to the soundboard specification

################## AMBIENT SOUND GROUPS ######################

A1 = [ # silence
      'clip00'
      ]

A3 = [ # Daytime
      'clip01', # Seagulls
      'clip02', # Seagulls
      'clip03', # Seagulls
      'clip04', # Seagulls
      'clip05', # Seagulls
      'clip06', # Bells
      'clip07', # Bells
      'clip08', # Bells
      'clip09', # Whistle
      'clip11', # Brody 
      'clip12', # Train 
      'clip13', # Train 
      'clip14', # Train 
      'clip39', # Seagulls
      'clip16', # Horn
      'clip17', # Horn
      'clip35', # Horn
      'clip36', # Horn
      ]

A4 = [ # Twlight, same as day + crickets + morning + geese - gulls
      'clip06', # Bells
      'clip07', # Bells
      'clip08', # Bells
      'clip09', # Whistle
      'clip11', # Brody 
      'clip12', # Train 
      'clip13', # Train 
      'clip14', # Train 
      'clip39', # Seagulls
      'clip16', # Horn
      'clip17', # Horn
      'clip18', # Cricket
      'clip19', # Cricket
      'clip20', # Morning
      'clip21', # Morning
      'clip35', # Horn
      'clip36', # Horn
      'clip37', # Geese
      'clip38'  # Geese
      ]

A5 = [ # Night time, daytime - gulls + crickets + owles
      'clip06', # Bell
      'clip07', # Bell
      'clip08', # Bell
      'clip09', # Whistle
      'clip11', # Brody
      'clip12', # Train
      'clip13', # Train
      'clip14', # Train
      'clip16', # Horn
      'clip17', # Horn
      'clip18', # Cricket
      'clip19', # Cricket
      'clip19', # Cricket
      'clip22', # Night
      'clip23', # Owl
      'clip24', # Owl
      'clip36', # Horn
      ]

D11 = [ # Stormy
      'clip27', # Thunder
      'clip27', # Thunder
      'clip28', # Thunder
      'clip28', # Thunder
      'clip29', # Thunder
      'clip30', # Wind
      'clip31', # Wind
      'clip31', # Wind
      'clip32', # Bells 
      'clip33', # Bells 
      'clip12', # Train
      'clip13', # Train
      'clip14', # Train
      'clip11', # Brody
      'clip35', # Horn
      'clip36', # Horn
      ]

D1 = [ # Stormy test
      'clip27',
      'clip28',
      'clip29',
      ]

################## VISUAL EFFECTS ######################
'''Possibly confusing: LIGHTING and LIGHTNING look very similar.'''

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
