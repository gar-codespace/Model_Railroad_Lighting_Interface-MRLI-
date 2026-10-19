import entities


class Sound:

    def __init__(self):

        self.uart:object = None

    def get_uart(self, specs:dict, tx=None, rx=None):

        id = specs['ID']
        baud = specs['BAUD_RATE']

        self.uart = entities.UART(id, baudrate=baud, tx=tx, rx=rx)

    def get_ambient_sound_board(self):

        self.ambient_sound_board = entities.SOUND_BOARD_DRIVER(entities.SOUND_BOARD, self.uart)

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
