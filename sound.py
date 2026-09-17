'''
Support methods for the controls library
Everything is here that involves the sound card.
'''

import entities

def get_sound_card(specs:tuple) -> object:

    board=specs[0]
    protocol=specs[1]

    return entities.SOUND_FX_LIBRARY(board, protocol)


def get_sound_clip():

    # print(getattr(entities, entities.SFX_GRP))
    
    sfx_group = getattr(entities, entities.SFX_GRP)
    group_count = len(sfx_group)
    select = entities.RANDINT(0, group_count - 1)
    sound_clip = sfx_group[select]
   
    return sound_clip

def get_pad():

    MIN_PAD = 2 # SECONDS
    MAX_PAD = entities.SFX_PAD

    pad = entities.RANDINT(MIN_PAD, MAX_PAD)

    return pad



        



