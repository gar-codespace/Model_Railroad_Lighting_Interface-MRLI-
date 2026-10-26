import entities
import model

'''
specs:
SOUND_CARD0 = {
            'BUS':'uart0',
            'PARAMS':'SB0',
            'DRIVER':'SOUND_DRIVER0'
            }
UART0 = {
          'TYPE':'uart',
          'ID':0,
          'TX':'COM2',
          'RX':COM3,
          'FREQ':9600
        }
SB0 = {
       'BOARD': 'Adafruit Sound FX Board',
       'WAIT':50,
       'DUPLEX':False
       }
'''

class Sound:

    def __init__(self, specs:dict):

        self.bus_params = getattr(entities, specs['BUS'])
        self.display_type = getattr(entities, specs['PARAMS'])
        self.driver = getattr(entities, specs['DRIVER'])

        self.bus:object = None
        self.board:object = None

        self.reset = self._set_reset_pin

    def _set_reset_pin(self):

        pin = None
        if self.display_type['RESET']:
            pin = entities.PIN(entities.PICO_PIN['RESET'], entities.PIN.IN)

        return pin

    def get_bus(self):

        attr = f'get_{self.bus_params['TYPE']}'
        self.bus = getattr(model, attr)(self.bus_params)

    def get_sound_board(self):

        self.sound_board = self.driver(self.display_type, self.bus, reset=self.reset)

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
