'''
Model Railroad Lighting Interface (MRLI)

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

    def __init__(self, params:dict):
    # Get the hardware parameters
        self.com = getattr(entities, params['COM'])
        self.params = getattr(entities, params['PARAMS'])
    # Import the driver library specified in self.params[DRIVER]
        driver = self.params['DRIVER']
        self.driver = __import__(driver).SoundFX
    # Make the bus type specified in self.params[BUS]
        attr = f'get_{self.com['TYPE']}'
        self.bus = getattr(model, attr)(self.com)
    # For this board there is a reset pin, but not always
        self.reset = self._set_reset_pin
        self.sound_board = self.driver(board=self.params, bus=self.bus, reset=self.reset)

    def _set_reset_pin(self):

        pin = None
        if self.params['RESET']:
            pin = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN)

        return pin

    def reset_sound_board(self):
        ...

    def _get_clip(self):

        clip = entities.AMBIENCE[entities.CLIP][0]

        return clip

    def _get_duration(self):

        duration = entities.AMBIENCE[entities.CLIP][1] * 1000 # ms

        return duration

    def play_sound(self) ->int:

        clip = self._get_clip()
        duration = self._get_duration()

        self.sound_board.play(clip)

        return duration

    def play_sound_now(self) ->int:

        clip = self._get_clip()
        duration = self._get_duration()

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
    entities.PROGRESS_MESSAGE = f'Sound Clip: {entities.AMBIENCE[entities.CLIP][2]}'

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
