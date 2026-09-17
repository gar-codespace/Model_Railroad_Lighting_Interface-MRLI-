'''
Support methods for the controls library
Everything is here that involves the sound card.
'''

import entities

def get_sound_card(specs):

    return entities.SOUND_FX_LIBRARY(board=specs[0], protocol=specs[1])




