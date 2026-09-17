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


        

    sfx_group = entities.A3
    group_count = len(sfx_group)
    select = entities.RANDINT(0, group_count - 1)
    sound_clip = sfx_group[select]

    return sound_clip

