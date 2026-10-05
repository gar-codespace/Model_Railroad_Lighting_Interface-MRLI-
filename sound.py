import entities

def get_ambient_sound_board(board:dict, bus:dict) -> object:

    ambient_sound_board = entities.SOUND_FX_DRIVER(board, bus)
    # ambient_sound_board.set_volume()

    return ambient_sound_board

def get_sound_clip() -> tuple:
    '''Randomly pick a sound clip from the sfx group.'''
    
    sfx_group = getattr(entities, entities.SFX_GRP)
    select = entities.RANDINT(0, len(sfx_group) - 1)
   
    return sfx_group[select]

def get_pad() -> int:
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
