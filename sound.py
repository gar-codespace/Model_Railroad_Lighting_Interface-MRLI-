import entities


class Sound:

    def __init__(self, UART):

        self.uart = UART

    def get_ambient_sound_board(self):

        self.ambient_sound_board = entities.SOUND_BOARD_DRIVER(entities.SOUND_BOARD, self.uart)

    def play_ambient_sound(self):

        clip = entities.AMBIENCE[entities.CLIP][0]
        duration = entities.AMBIENCE[entities.CLIP][1] * 1000 # ms
        description = entities.AMBIENCE[entities.CLIP][2]

        self.ambient_sound_board.play_now(clip)

        print(f'Ambient Clip: {clip} - {description}')

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
