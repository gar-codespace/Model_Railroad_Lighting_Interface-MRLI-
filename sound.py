import entities

'''
parameters of sound_board:
SB0 = {
       'BOARD': 'Adafruit Sound FX Board',
       'TYPE':'uart',
       'WAIT':50,
       'DUPLEX':False
       }
UART0 = {
          'ID':0,
          'BAUD_RATE':9600
        }
'''

class Sound:

    def __init__(self, board:dict, bus:dict, reset:object=None):

        self.board = board

        self.bus:object = None
        self.type = board['TYPE']
        self.reset = reset

        self.id = bus['ID']
        self.freq = bus['FREQ']

    def get_bus(self, pin0=None, pin1=None):
        '''This can be decorated for different bus types.'''

        if self.type == 'uart':
            id = self.id
            baud = self.freq
            self.bus = entities.UART(id, baudrate=baud, tx=pin0, rx=pin1)

    def get_ambient_sound_board(self):

        self.ambient_sound_board = entities.SOUND_BOARD_DRIVER(self.board, self.bus, self.reset)

    def play_ambient_sound(self) ->int:

        clip = entities.AMBIENCE[entities.CLIP][0]
        duration = entities.AMBIENCE[entities.CLIP][1] * 1000 # ms

        self.ambient_sound_board.play_now(clip)

        return duration


def get_ambient_clip() -> tuple:
    '''Randomly pick a sound clip from the ambient sounds group.'''
    
    ambient_group = getattr(entities, entities.CLIP_G)
    select = entities.RANDINT(0, len(ambient_group) - 1)

    entities.CLIP = ambient_group[select]

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
