'''
Model Railroad Lighting Interface (MRLI)
The sound driver library is imported here.

params:
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

import entities
import model


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
        duration = entities.AMBIENCE[entities.CLIP][1] * 1000 # ms

        self.sound_board.play(clip)

        return duration

    def play_sound_now(self) ->int:

        clip = entities.AMBIENCE[entities.CLIP][0]
        duration = entities.AMBIENCE[entities.CLIP][1] * 1000 # ms

        self.sound_board.play_now(clip)

        return duration

    def stop_sound(self):

        self.sound_board.stop()

        return


def get_ambient_clip() -> tuple:
    '''Randomly pick a sound clip from the ambient sounds group.'''
    
    ambient_group = getattr(entities, entities.CLIP_G)
    select = entities.RANDINT(0, len(ambient_group) - 1)

    entities.CLIP = ambient_group[select]
    entities.LOGGING_MESSAGE = [f'Sound Clip: {entities.AMBIENCE[entities.CLIP][2]}']

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
