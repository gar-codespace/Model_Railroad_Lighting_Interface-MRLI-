'''
Support methods for the controls library
Everything is here that involves the sound card.
'''

import entities

def get_sound_card(uart, board):

    return entities.SoundFX(uart=uart,board=board)




