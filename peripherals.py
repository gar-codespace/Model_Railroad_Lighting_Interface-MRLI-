'''
Model Railroad Lighting Interface (MRLI)
The display driver library is imported here.
The sound driver library is imported here.
'''

import entities
import model
import states


'''
display specs:
DISPLAY_0 = {
            'NAME':'1.3" OLED Display',
            'COM':'I2C_0',
            'PARAMS':'OLED_0',
            }
I2C_0 = {
          'TYPE':'i2c',
          'ID':0,
          'SDA':'COM0',
          'SCL':'COM1',
          'FREQ':400000
        }
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
'''

class Display:

    def __init__(self, specs:dict):
    # Get the hardware parameters
        com = getattr(entities, specs['COM'])
        params = getattr(entities, specs['PARAMS'])
    # Import the driver library specified in params[DRIVER]
        driver = __import__(params['DRIVER']).Driver
    # Make the bus type specified in params[BUS]
        attr = f'get_{com['TYPE']}'
        bus = getattr(model, attr)(com)

        self.display = driver(params=params, bus=bus)
        
    def update_display(self, content:list = None):

        self.display.fill(0)
        self.display.contrast(entities.MAIN_DISPLAY_BRIGHT)

        line_y = entities.MAIN_FORMAT['Y_OFFSET'] # vertically center the text in the display
        for i in range(entities.MAIN_FORMAT['ROWS']):
            self.display.text(content[i], entities.MAIN_FORMAT['X_OFFSET'], line_y)
            line_y += entities.MAIN_FORMAT['LINE_HEIGHT']

        try: # add the hilight rectangle
            attrib = f'{entities.MACHINE_STATE}_get_hilight'
            rect = getattr(states, attrib)()
            self.display.rect(rect[0], rect[1], rect[2], rect[3], rect[4])
        except:
            pass

        self.display.show()

'''
sound specs:
SOUND_CARD_0 = {
            'COM':'UART_0',
            'PARAMS':'SB_0',
            }
UART_0 = {
          'TYPE':'uart',
          'ID':0,
          'TX':'COM2',
          'RX':COM3,
          'FREQ':9600
        }
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
'''

class Sound:

    def __init__(self, specs:dict):
    # Get the hardware parameters
        com = getattr(entities, specs['COM'])
        params = getattr(entities, specs['PARAMS'])
    # Import the driver library specified in params[DRIVER]
        driver = __import__(params['DRIVER']).Driver
    # Make the bus type specified in params[BUS]
        attr = f'get_{com['TYPE']}'
        bus = getattr(model, attr)(com)
    # For this board there is a reset pin, but not always
        reset = None
        if params['RESET']:
            reset = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN)

        self.sound_board = driver(params=params, bus=bus, reset=reset)

    def reset_sound_board(self):
        ...

    def play_sound(self) ->int:

        clip = entities.AMBIENCE[entities.CLIP][0]

        self.sound_board.play(clip)

    def play_sound_now(self) ->int:

        clip = entities.AMBIENCE[entities.CLIP][0]

        self.sound_board.play_now(clip)

    def stop_sound(self):

        self.sound_board.stop()

        return
    