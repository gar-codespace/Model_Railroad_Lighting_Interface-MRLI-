import entities

def get_sound_card(board:dict, bus:dict, reset_pin:object=None) -> object:

    sound_card = entities.SOUND_DRIVER(board, bus, reset_pin)
    sound_card.initialize_board()

    return sound_card

def get_sound_clip():
    
    sfx_group = getattr(entities, entities.SFX_GRP)
    group_count = len(sfx_group)
    select = entities.RANDINT(0, group_count - 1)
    sound_clip = sfx_group[select]
   
    return sound_clip

def get_pad():
    '''A random ammount of time between sound clips (seconds).'''

    pad = entities.RANDINT(entities.PAD_MIN, entities.PAD_MAX)

    return pad
