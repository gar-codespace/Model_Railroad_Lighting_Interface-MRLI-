import entities

def get_sound_card(board:dict, bus:dict, reset_pin:object=None) -> object:

    sound_card = entities.SOUND_DRIVER(board, bus, reset_pin)
    sound_card.initialize_board()

    return sound_card

def get_sound_clip():
    '''Randomly pick a sound clip from the sfx group.'''
    
    sfx_group = getattr(entities, entities.SFX_GRP)
    select = entities.RANDINT(0, len(sfx_group) - 1)
   
    return sfx_group[select]

def get_pad():
    '''A random ammount of time between sound clips (ms).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
