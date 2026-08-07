'''
Support methods for the controls library
Everything is here that involves the sound card.
'''

import entities

def get_sound_card():

    i2c = entities.I2C(1, sda=26, scl=27, freq=400000)

    return entities.MAX9744(i2c)



def play_welcome_sound(sound_card):

    pass



