import entities

def get_ambient_sound_board(board:dict, bus:dict) -> object:

    ambient_sound_board = entities.SOUND_BOARD_DRIVER(board, bus)
    # ambient_sound_board.set_volume()

    return ambient_sound_board

def get_ambient_clip() -> tuple:
    '''Randomly pick a sound clip from the ambient sounds group.'''
    
    ambient_group = getattr(entities, entities.CLIP_G)
    select = entities.RANDINT(0, len(ambient_group) - 1)

    entities.CLIP = ambient_group[select]

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
