'''
Support methods for the controls library
Everything is here that involves the sound card.
'''

import entities

class SFX:

    def __init__(self):
        pass

    def unmute(self):
        pass

    def mute(self):
        pass

    def get_sfx(self):

        sfx_group = entities.SFX_GRP
        sfx_count = len(sfx_group)
        select_sfx_index = entities.RANDINT(0, sfx_count - 1)
        entities.SFX_NAME = entities.SFX_GRP[select_sfx_index]

    def play_sfx(self):
        pass




